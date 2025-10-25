from tkinter import *


def login():    
    nome
    senha
    cpf
    
def esqueci_senha():
    senha_nova

def cadastro():
    cad

def sair():
    TelaMain.destroy()

#CODIGO
#Cria a tela inicial
TelaMain = Tk()

#Ttitulo da tela
TelaMain.title("")

#Logo parte superior
logoicon = PhotoImage(file="chave.png")
Label(TelaMain,image=logoicon).grid(column=0, row=0, padx=30, pady=30)

#Texto de boas vindas
texto1 = Label(TelaMain, text="Olá bem vindo ao nota dez\n Faça seu login abaixo", font="Arial 15 bold")
texto1.grid(column= 0, row=1)

#Frame do background dos Entrys e Labels
frame1 = Frame(TelaMain)

fundo_main = Label(frame1, bg="#ddf5ff", height="10", width="50", borderwidth= 0.5, relief="solid")
fundo_main.grid(column= 0, row = 2, columnspan=2)

fundo_entry = Label(frame1, bg="#9bdafd", height="2", width="45", borderwidth= 1, relief="solid")
fundo_entry.place(x= 18, y=15)

fundo_entry2 = Label(frame1, bg="#9bdafd", height="2", width="45", borderwidth= 1, relief="solid")
fundo_entry2.place(x= 18, y=65)

#Textos identificadores do campos
texto_Nome = Label(frame1, text="Nome:", font="Arial 15", background="#9bdafd")
texto_Nome.place(x= 25, y=17)

texto_Senha = Label(frame1, text="Senha:", font="Arial 15", background="#9bdafd")
texto_Senha.place(x= 25, y=67)

#Campos para o user digitar
campo_nome = Entry(frame1, textvariable="", width="25")
campo_nome.place(x=170, y=23)

campo_senha= Entry(frame1, textvariable="", width="25")
campo_senha.place(x=170, y=73)

#Botões 
btn_login = Button(frame1, text="Login", command=login, font="Arial 13",  width="14", bg="#9bdafd", borderwidth=1, relief="solid")
btn_login.place(x=205, y=120)

btn_esqueci_senha = Button(frame1, text="Esqueci senha", font="Arial 13", command=esqueci_senha, width="14", bg="#9bdafd", borderwidth=1, relief="solid")
btn_esqueci_senha.place(x=18, y=120)

#Texto de primeiro acesso
texto_primeiro_acesso = Label(TelaMain, text="Primeiro Acesso?\n Faça seu cadastro apertando o botão abaixo", font="Arial 15 bold")
texto_primeiro_acesso.grid(column= 0, row=3)

btn_cadastro = Button(TelaMain, text="Cadastro", font="Arial 14", command=cadastro,  width="18", bg="#9bdafd", borderwidth=1, relief="solid")
btn_cadastro.grid(column=0, row=4)

btn_sair = Button(TelaMain, text="Sair", font="Arial 14", command=sair,  width="18", bg="#9bdafd", borderwidth=1, relief="solid")
btn_sair.grid(column=0, row=5)

frame1.grid(column=0, row=2)
frame1.columnconfigure((0,4), weight=1)
frame1.rowconfigure((1,2,3),weight=0)
frame1.rowconfigure(0, weight=0)
frame1.rowconfigure(tuple(range(1,7)), weight=0, pad=5)
frame1.rowconfigure(8,weight=1)

TelaMain.columnconfigure((0,4), weight=1)
TelaMain.rowconfigure((1,2,3),weight=0)
TelaMain.rowconfigure(0, weight=0)
TelaMain.rowconfigure(tuple(range(1,7)), weight=0, pad=5)
TelaMain.rowconfigure(8,weight=1)


TelaMain.geometry("500x500")
TelaMain.mainloop()
    