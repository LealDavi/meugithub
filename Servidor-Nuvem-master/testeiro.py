import socket
from tkinter import *
import hashlib
import os

host = "127.0.0.1"
port = 6060
usuario = ""
senha = ""

def interface_grafica():

    def codificar_u_s(usuario, senha):

        # Adiciona usuario e senha a uma lista
        u = hashlib.md5(bytes(usuario, "utf-8")).hexdigest()
        s = hashlib.md5(bytes(senha, "utf-8")).hexdigest()
        usuario_senha = [u, s]

        # Converte lista em string
        usuario_senha = ",".join(usuario_senha)
        return usuario_senha


    def main(escolha, usuario, senha):

        def script_de_retorno():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            print("conectou")
            sock.send("entrar".encode("utf-8"))
            print("enviou")
            sock.send(codificar_u_s(usuario, senha).encode("utf-8"))
            print("codificou e enviou")
            autenticacao = sock.recv(10).decode("utf-8")
            print("recebeu")
            segundaTela(sock)

        def segundaTela(sock):

            def download(texto):

                sock.send("recebe".encode("utf-8"))
                sock.send(texto.encode("utf-8"))
                with open("r_" + texto, "wb") as f:
                    while True:
                        l = sock.recv(1024)
                        if not l:
                            print("Download concluido")
                            break
                        f.write(l)
                script_de_retorno()

            def tela_enviar_para_o_servidor():

                def enviar_para_o_servidor():

                    sock.send("enviar".encode("utf-8"))
                    indice = listbox_enviar.curselection()[0]
                    texto = listbox_enviar.get(indice)

                    #Envia o nome do arquivo enviado
                    sock.send(texto.encode("utf-8"))
                    f = open(texto, "rb")
                    l = f.read(1024)
                    while l:
                        sock.send(l)
                        l = f.read(1024)
                    print("Envio Concluido")
                    f.close()
                    telaUpload.destroy()
                    script_de_retorno()

                telaUsuario.destroy()
                telaUpload = Tk()
                telaUpload["background"] = "white"

                fonte_padrao = ("helvetica", "12", "bold")

                primeiro_container_enviar = Frame(telaUpload, background="#0277bd", padx=80)
                titulo = Label(primeiro_container_enviar, text="Armazenamento em Nuvem", background="#0277bd", foreground="#ffffff", font=("helvetica", 18, "bold"))
                titulo.pack(pady=(40, 40))
                primeiro_container_enviar.pack()

                segundo_container_enviar = Frame(telaUpload, background="white", padx=10, pady=20)
                segundo_container_enviar.pack()

                button = Button(segundo_container_enviar, command=enviar_para_o_servidor, text="Upload", width=20, background="#0277bd", foreground="#ffffff", activebackground="#58a5f0", font=(fonte_padrao, 13, "bold"), padx=10)
                button.grid(column=0, row=2)

                Label(segundo_container_enviar, text="Arquivos do Usuario", bg="white", font=fonte_padrao).grid(column=0, row=0)

                listbox_enviar = Listbox(segundo_container_enviar)
                listbox_enviar['width'] = 37

                arquivos = os.listdir()

                for item in arquivos:
                    listbox_enviar.insert(END, item)
                listbox_enviar.grid(column=0, row=0)
                mensagem_de_erro_enviar = Label(telaUpload, text="", bg="white", font=fonte_padrao)
                mensagem_de_erro_enviar.pack()
                telaUpload.mainloop()
            def st_capturar():
                try:
                    mensagem_de_erro["text"] = ""
                    indice = listbox.curselection()[0]
                    texto = listbox.get(indice)
                    print(texto)
                    download(texto)
                except:
                    mensagem_de_erro["text"] = "Escolha arquivo para download"

            def enviarSair():
                telaUsuario.destroy()
                interface_grafica()

            data = sock.recv(1024).decode("utf-8")
            lista = data.split(",")

            telaUsuario = Tk()
            telaUsuario["background"] = "white"

            fonte_padrao = ("helvetica", "12", "bold")

            primeiro_container = Frame(telaUsuario, background="#0277bd", padx=80)
            titulo = Label(primeiro_container, text="Armazenamento em Nuvem", background="#0277bd", foreground="#ffffff", font=("helvetica", 18, "bold"))
            titulo.pack(pady=(40, 40))
            primeiro_container.pack()

            segundo_container = Frame(telaUsuario, background="white", padx=10, pady=20)
            segundo_container.pack()

            button = Button(segundo_container, command=st_capturar, text="Download", width=20, background="#0277bd", foreground="#ffffff", activebackground="#58a5f0", font=(fonte_padrao, 13, "bold"), padx=10)
            button.grid(column=0, row=1)

            button = Button(segundo_container, command=tela_enviar_para_o_servidor, text="Upload", width=20, background="#0277bd", foreground="#ffffff", activebackground="#58a5f0", font=(fonte_padrao, 13, "bold"), padx=10)
            button.grid(column=0, row=2)

            button = Button(segundo_container, command=enviarSair, text="Sair", width=20, background="#0277bd", foreground="#ffffff", activebackground="#58a5f0", font=(fonte_padrao, 13, "bold"), padx=10)
            button.grid(column=0, row=3)

            Label(segundo_container, text="Arquivos do Usuario", bg="white", font=fonte_padrao).grid(column=0, row=0)

            listbox = Listbox(segundo_container)
            listbox['width'] = 37

            for item in lista:
                listbox.insert(END, item)
            listbox.grid(column=0, row=0)
            mensagem_de_erro = Label(telaUsuario, text="", bg="white", font=fonte_padrao)
            mensagem_de_erro.pack()


        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        if escolha == "entrar":

            sock.send(escolha.encode("utf-8"))

            #Envia lista com usuario e senha codificado
            sock.send(codificar_u_s(usuario, senha).encode("utf-8"))

            # Recebe true(Usuario autenticado)
            autenticacao = sock.recv(10).decode("utf-8")

            if autenticacao == "verdadeiro":
                print("Parabens")
                master.destroy()
                segundaTela(sock)

            else:
                mensagem["text"] = "Usuário e senha incorretos"
                sock.close()

        if escolha == "cadast":
            print("entrou cadastrar")
            print(escolha)
            sock.send(escolha.encode("utf-8"))

            # Envia lista com usuario e senha codificado
            sock.send(codificar_u_s(usuario, senha).encode("utf-8"))

            autenticacao = sock.recv(6).decode("utf-8")
            if autenticacao == "negado":
                mensagem["text"] = "Usuário já existe"
            else:
                mensagem["text"] = "Cadastrado com sucesso"

    def entrar():
        nomeUsuario = usuario.get()
        senhaUsuario = senha.get()
        usuario.delete(0, END)
        senha.delete(0, END)
        main("entrar", nomeUsuario, senhaUsuario)
    def cadastrar(usuario, senha):
        main("cadast", usuario, senha)

    def chamar_cadastro(event):

        def voltar(event):
            telaCadastro.destroy()

        def pre_cadastrar():

            usuario = nomeCadastro.get()
            senha = senhaCadastro.get()
            senha2 = senhaCadastro2.get()
            nomeCadastro.delete(0, END)
            senhaCadastro.delete(0, END)
            senhaCadastro2.delete(0, END)
            if senha == senha2:
                if usuario != "":
                    mensagemCadastro["text"] = "Cadastrado com sucesso"
                    cadastrar(usuario, senha)
                else:
                    mensagemCadastro["text"] = "Campo 'usuario' vazio"
            else:
                mensagemCadastro["text"] = "Senhas não coincidem"

        usuario.delete(0, END)
        senha.delete(0, END)
        mensagem["text"] = ""

        telaCadastro = Tk()
        telaCadastro["background"] = "white"

        fontePadrao = ("helvetica", "12", "bold")

        primeiroContainer = Frame(telaCadastro, padx=80, background="#0277bd")
        titulo = Label(primeiroContainer, background="#0277bd", foreground="#ffffff", text="Armazenamento em Nuvem", font=("helvetica", 18, "bold"))
        titulo.pack(pady=(40, 40))
        primeiroContainer.pack()

        segundoContainer = Frame(telaCadastro, background="white", width=356, height=200)
        Label(segundoContainer, text="Usuário", font=fontePadrao, background="white").grid(column=0, row=1)
        Label(segundoContainer, text="Senha", font=fontePadrao, background="white").grid(column=0, row=2)
        Label(segundoContainer, text="Confirmar Senha", font=fontePadrao, background="white").grid(column=0, row=3)
        nomeCadastro = Entry(segundoContainer)
        nomeCadastro.grid(column=1, row=1)
        senhaCadastro = Entry(segundoContainer, show="*")
        senhaCadastro2 = Entry(segundoContainer, show="*")
        senhaCadastro.grid(column=1, row=2)
        senhaCadastro2.grid(column=1, row=3)
        segundoContainer.pack(pady=20)

        terceiroContainer = Frame(telaCadastro, background="white", padx=10, pady=2)
        terceiroContainer.pack()

        button = Button(terceiroContainer, command=pre_cadastrar, text="Cadastrar", width=31, background="#0277bd", foreground="#ffffff", activebackground="#58a5f0", font=(fontePadrao, 13, "bold"), padx=10)
        button.pack(pady=(20, 0))

        link = Label(terceiroContainer, text="Voltar", fg="blue", bg="white", cursor="hand2")
        link.pack(pady=(10, 10))
        link.bind("<Button-1>", voltar)

        mensagemCadastro = Label(terceiroContainer, text="", font=fontePadrao, bg="white")
        mensagemCadastro.pack()

        telaCadastro.mainloop()

    #Interface gráfica
    master = Tk()
    master["background"] = "white"

    fontePadrao = ("helvetica", "12", "bold")

    primeiro_container = Frame(master, padx="80", background="#0277bd")
    titulo = Label(primeiro_container, background="#0277bd", foreground="#ffffff", text="Armazenamento em Nuvem", font=("helvetica",18,"bold"))
    titulo.pack(pady=(40, 40))
    primeiro_container.pack()

    segundo_container = Frame(master, background="white", width=356)
    Label(segundo_container, text="Usuário", font=fontePadrao, background="white").grid(column=0, row=1)
    Label(segundo_container, text="Senha", font=fontePadrao, background="white").grid(column=0, row=2)
    usuario = Entry(segundo_container)
    usuario.grid(column=1, row=1)
    senha = Entry(segundo_container, show="*")
    senha.grid(column=1, row=2)
    segundo_container.pack(pady=20)

    terceiro_container = Frame(master, background="white", padx=10, pady=2)
    terceiro_container.pack()

    button = Button(terceiro_container, command=entrar, text="Entrar", width=31, background="#0277bd", foreground="#ffffff", activebackground="#58a5f0", font=("helvetica", 13,"bold"), padx=10)
    button.pack(pady=(20, 0))

    link = Label(terceiro_container, text="Não possui uma conta?", background="white", fg="blue", cursor="hand2")
    link.pack(pady=(10, 10))
    link.bind("<Button-1>", chamar_cadastro)

    mensagem = Label(terceiro_container, text="", bg="white", font=fontePadrao)
    mensagem.pack()

    master.mainloop()
interface_grafica()

