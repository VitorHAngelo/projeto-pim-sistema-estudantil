import tkinter as tk
from tkinter import ttk, messagebox
from config import FILES_PATH
from datetime import datetime

TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def ui_login(janela: tk.Tk):
    alt_tamanho_janela(janela, 500, 500)
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
    escrita = """
   █████████                                       █████    ██████████     █████           
  ███░░░░░███                                     ░░███    ░░███░░░░░█    ░░███            
 ░███    ░░░  █████████████    ██████   ████████  ███████   ░███  █ ░   ███████  █████ ████
 ░░█████████ ░░███░░███░░███  ░░░░░███ ░░███░░███░░░███░    ░██████    ███░░███ ░░███ ░███ 
  ░░░░░░░░███ ░███ ░███ ░███   ███████  ░███ ░░░   ░███     ░███░░█   ░███ ░███  ░███ ░███ 
  ███    ░███ ░███ ░███ ░███  ███░░███  ░███       ░███ ███ ░███ ░   █░███ ░███  ░███ ░███ 
 ░░█████████  █████░███ █████░░████████ █████      ░░█████  ██████████░░████████ ░░████████
  ░░░░░░░░░  ░░░░░ ░░░ ░░░░░  ░░░░░░░░ ░░░░░        ░░░░░  ░░░░░░░░░░  ░░░░░░░░   ░░░░░░░░ 
"""
    label_escrita = tk.Label(
        logo_frame, text=escrita, font=("Consolas", 10), justify="left"
    )
    label_escrita.grid(row=0, column=1, sticky="sw")
    ttk.Separator(frame_conteudo, orient=tk.HORIZONTAL).grid(
        row=1, column=0, columnspan=10, sticky="nwe"
    )


def limpar_widgets(janela: tk.Tk):
    for widget in janela.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()


def encerrar(janela):
    if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
        janela.concluido.set(True)
        janela.quit()
        janela.after(50, janela.destroy)


def alt_tamanho_janela(janela: tk.Tk, width: int, height: int):
    janela.update_idletasks()

    x = (janela.winfo_screenwidth() // 2) - (width // 2)
    y = (janela.winfo_screenheight() // 2) - (height // 2)

    janela.geometry(f"{width}x{height}")
    janela.update_idletasks()

    janela.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


def formatar_telefone(event, campo, entry):
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
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
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
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


def verificar_email(event, campo, entry):
    email = list(campo.get())
    if not "@" in email or not "." in email or " " in email:
        entry.config(fg="red")
    else:
        entry.config(fg="black")


def verificar_data(event, campo, entry):
    if event.state in (40, 262184) and event.keysym in TECLAS_IGNORADAS:
        return
    data = [letter for letter in campo.get() if letter.isdigit()]
    if event.state == 40 and event.keysym == "Tab" and len(data) == 6:
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
