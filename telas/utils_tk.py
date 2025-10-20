import tkinter as tk
from tkinter import ttk
from config import FILES_PATH


def fechar(janela: tk.Tk):
    if hasattr(janela, "concluido"):
        janela.concluido.set(True)
    janela.destroy()


def ui_login(janela: tk.Tk):
    janela.geometry("500x500")
    janela.title("Sistema Estudantil")
    janela.iconbitmap(FILES_PATH + "SmartEdu.ico")
    janela.login_logo_frame = tk.Frame(janela, height=300, width=300)
    janela.login_logo_frame.grid(row=0, column=0, sticky="n")
    logo = tk.PhotoImage(file=FILES_PATH + "SmartEdu.png")
    label_logo = tk.Label(janela.login_logo_frame, image=logo)
    label_logo.img = logo
    label_logo.grid(row=0, column=0, sticky="we", pady=(50,))


def ui_geral(frame_conteudo: tk.Tk):
    logo_frame = tk.Frame(frame_conteudo, width=1500, padx=10)
    # logo_frame.rowconfigure(0, minsize=10, weight=0)
    logo_frame.columnconfigure(0, minsize=100, weight=1)
    logo_frame.columnconfigure(10, minsize=2000)
    logo_frame.grid(row=0, column=0, sticky="wse")
    logo = tk.PhotoImage(file=FILES_PATH + "SmartEdu.png")
    label_logo = tk.Label(logo_frame, image=logo)
    label_logo.img = logo
    label_logo.grid(
        row=0,
        column=0,
        padx=0,
        pady=0,
    )
    ttk.Separator(frame_conteudo, orient=tk.HORIZONTAL).grid(
        row=1, column=0, columnspan=10, sticky="nwe"
    )


def limpar_widgets(janela: tk.Tk):
    for widget in janela.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()
