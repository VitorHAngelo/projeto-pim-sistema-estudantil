import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from config import FILES_PATH
from datetime import datetime
import re
import contexto

TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def ui_login():
    alt_tamanho_janela(500, 500)
    contexto.janela.title("EduSmart")
    contexto.janela.iconbitmap(FILES_PATH + "EduSmart.ico")
    contexto.janela.login_logo_frame = tk.Frame(contexto.janela, height=300, width=300)
    contexto.janela.login_logo_frame.grid(row=0, column=0, sticky="n")
    logo = tk.PhotoImage(file=FILES_PATH + "EduSmart.png")
    label_logo = tk.Label(contexto.janela.login_logo_frame, image=logo)
    label_logo.img = logo
    label_logo.grid(row=0, column=0, sticky="we", pady=(50,))


def ui_geral():
    logo_frame = tk.Frame(contexto.frame_conteudo, width=1500, padx=10)
    logo_frame.columnconfigure(0, minsize=100, weight=1)
    logo_frame.columnconfigure(10, minsize=2000)
    logo_frame.grid(row=0, column=0, sticky="wse")
    logo = tk.PhotoImage(file=FILES_PATH + "EduSmart.png")
    label_logo = tk.Label(logo_frame, image=logo)
    label_logo.img = logo
    label_logo.grid(
        row=0,
        column=0,
        padx=0,
        pady=0,
    )
    ttk.Separator(contexto.frame_conteudo, orient=tk.HORIZONTAL).grid(
        row=1, column=0, columnspan=10, sticky="nwe"
    )


def limpar_widgets(frame=None):
    """Destrói widgets.

    Se `frame` for fornecido, destrói os filhos desse frame; caso contrário
    destrói os filhos da janela principal (`contexto.janela`). Ignora menus.
    """
    # Por compatibilidade: quando nenhum frame for passado, limpe o
    # `contexto.frame_conteudo` (área principal de conteúdo) se disponível;
    # caso contrário, caia para a janela principal. Isso evita destruir widgets
    # globais (menus, login frames) que residem em `contexto.janela`.
    target = (
        frame
        if frame is not None
        else (
            contexto.frame_conteudo
            if getattr(contexto, "frame_conteudo", None)
            else contexto.janela
        )
    )

    # Segurança: se target for None ou não possuir winfo_children, apenas retorna
    if target is None or not hasattr(target, "winfo_children"):
        return

    for widget in target.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()


def encerrar():
    if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
        contexto.janela.concluido.set(True)
        contexto.janela.quit()
        contexto.janela.after(50, contexto.janela.destroy)


def alt_tamanho_janela(width: int, height: int):
    contexto.janela.update_idletasks()

    if (
        contexto.janela.winfo_screenwidth() <= 1366
        or contexto.janela.winfo_screenheight() <= 768
    ) and width > 500:
        contexto.janela.state("zoomed")
    else:
        contexto.janela.state("normal")
        x = (contexto.janela.winfo_screenwidth() // 2) - (width // 2)
        y = (contexto.janela.winfo_screenheight() // 2) - (height // 2)

        contexto.janela.geometry(f"{width}x{height}")
        contexto.janela.update_idletasks()

        contexto.janela.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


def formatar_telefone(event, campo, entry):
    if event:
        if event.keysym in TECLAS_IGNORADAS:
            return
    telefone = [char for char in campo.get() if char.isdigit()]
    if len(telefone) == 10:
        telefone.insert(0, "(")
        telefone.insert(3, ")")
        telefone.insert(8, "-")
        entry.delete(0, tk.END)
        entry.insert(0, "".join(telefone))
    else:
        telefone.insert(0, "(")
        telefone.insert(3, ")")
        telefone.insert(9, "-")
        entry.delete(0, tk.END)
        entry.insert(0, "".join(telefone[0:14]))


def formatar_cpf(event, campo, entry):
    if event:
        if event.keysym in TECLAS_IGNORADAS:
            return
    cpf = [char for char in campo.get() if char.isdigit()]
    if len(cpf) >= 3:
        cpf.insert(3, ".")
    if len(cpf) >= 6:
        cpf.insert(7, ".")
    if len(cpf) >= 9:
        cpf.insert(11, "-")
    entry.delete(0, tk.END)
    entry.insert(0, "".join(cpf[:14]))


def verificar_email(campo, event=None, entry=None):
    padrao_email = r"^[A-Za-z0-9._%+-]{3,}@[A-Za-z0-9.-]{3,}\.[A-Za-z]{2,}$"
    valido = re.match(padrao_email, campo.get().lower())
    if valido:
        if entry:
            entry.config(fg="black")
        return True
    else:
        if entry:
            entry.config(fg="red")
        return False


def verificar_data(event, campo, entry):
    data = [letter for letter in campo.get() if letter.isdigit()]
    if event:
        if event.keysym in TECLAS_IGNORADAS:
            return
    else:
        print("Sem evento.")
        data.insert(2, "/")
        data.insert(5, "/")
        entry.delete(0, tk.END)
        entry.insert(0, "".join(data[:10]))
        return

    if event.keysym == "Tab" and len(data) == 6:
        if int("".join(data[-2:])) <= int(str(datetime.now().year)[2:]):
            entry.insert(6, 20)
        else:
            entry.insert(6, 19)
        return
    if len(data) > 1:
        data.insert(2, "/")
    if len(data) > 4:
        data.insert(5, "/")
    entry.delete(0, tk.END)
    entry.insert(0, "".join(data[:10]))
