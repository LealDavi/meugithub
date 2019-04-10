import socket
import os
import json
import threading

host = ''
port = 6060

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen(5)

def salvar(dicionario):
    with open('data.json', 'w') as f:
        json.dump(dicionario, f)

def incluir_cliente_no_server(titulo, descricao):
    try:
        with open('data.json', 'r') as f:
            dicionario = json.load(f)
            dicionario[titulo] = descricao
            salvar(dicionario)
    except:
        dicionario = {}
        dicionario[titulo] = descricao
        salvar(dicionario)

def criar_diretorio(usuario):
    os.mkdir("arquivosDeUsuario/" + usuario)
    with open("arquivosDeUsuario/" + usuario + "/leiame.txt", "w") as f:
        f.write("Bem vindo ao servidor de arquivos em nuvem")

def enviar_para_o_cliente(usuario):
        texto = conn.recv(1024).decode("utf-8")
        try:
            f = open("arquivosDeUsuario/" + usuario + "/" + texto, "rb")
            l = f.read(1024)
            while l:
                conn.send(l)
                l = f.read(1024)
            print("Download Concluido")
            f.close()
        except:
            print("Conexão encerrada porque usuario desconectou")


def receber_do_cliente(usuario):
    nome_arquivo = conn.recv(1024).decode("utf-8")
    print("receber")#"arquivosDeUsuario/" + usuario + "/" + nome_arquivo
    print("usuario: " + usuario)
    with open("arquivosDeUsuario/" + usuario + "/" + nome_arquivo, "wb") as f:
        print("aberto")
        while True:
            print("entrou no while")
            conn.settimeout(5.0)
            l = conn.recv(1024)
            print(l)
            if not l:
                print("Recebimento concluido")
                break
            print("f.write")
            f.write(l)

def extrair_usuario_senha(usuario_senha):

    print(usuario_senha)
    lista = usuario_senha.split(",")
    return lista[0], lista[1]

def verificarAutenticacao(usuario, senha):
    with open("data.json", "r") as f:
        dicionario = json.load(f)
        for x, y in dicionario.items():
            if x == usuario:
                if y == senha:
                    return "verdadeiro"
                else:
                    return 0
        return 0

def verificarAutenticacaoUsuario(usuario):
    with open("data.json", "r") as f:
        dicionario = json.load(f)
        for x, y in dicionario.items():
            print("x: " + x)
            print("u: " + usuario)
            if x == usuario:
                return "verdadeiro"
        return 0


def handle_client(conn,addr):
    controle = conn.recv(6).decode("utf-8")
    print("controle: " + controle)
    if controle == "cadast":
        print("cadastrar")
        usuario_senha = conn.recv(500).decode("utf-8")
        usuario, senha = extrair_usuario_senha(usuario_senha)
        # Verifica se usuario e senha recebidos estao cadastrados
        autenticacao = verificarAutenticacaoUsuario(usuario)
        print(autenticacao)
        if autenticacao == "verdadeiro":
            print("Usuario ja existe")
            conn.send("negado".encode("utf-8"))
        else:
            conn.send("aprova".encode("utf-8"))
            print("extraido")
            incluir_cliente_no_server(usuario, senha)
            criar_diretorio(usuario)
            print("incluso novo cliente")

    if controle == "entrar":
        print("entrar")
        usuario_senha = conn.recv(500).decode("utf-8")
        usuario, senha = extrair_usuario_senha(usuario_senha)

        #Verifica se usuario e senha recebidos estao cadastrados
        autenticacao = verificarAutenticacao(usuario, senha)

        if autenticacao == "verdadeiro":
            try:
                conn.send(autenticacao.encode("utf-8"))

                diretorios = ",".join(os.listdir("arquivosDeUsuario/" + usuario))
                conn.send(diretorios.encode("utf-8"))
                decisao = conn.recv(6).decode("utf-8")
                if decisao == "recebe":
                    enviar_para_o_cliente(usuario)
                elif decisao == "enviar":
                    print("entrou_enviar")
                    receber_do_cliente(usuario)
                conn.close()
            except:
                print("Usuario desconectado")
        else:
            conn.close()
            print("Usuario nao autenticado")

while True:

    conn, addr = sock.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.start()