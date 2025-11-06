import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from seguranca import verificar_senha, hashear_senha
from telas.utils_tk import limpar_widgets
from dados import editar_colaborador
from config import GUI_FONT
import contexto

TECLAS_IGNORADAS = ("BackSpace", "Delete", "Left", "Up", "Down", "Right", "Return")


def limpar():
    frame_alterar_senha.destroy()


def salvar(event, colaborador):
    status = verificar_senha(colaborador["senha"], senhas["atual"].get())
    if status == 0:
        if senhas["nova"].get() == senhas["repita"].get():
            if len(senhas["nova"].get()) >= 8:
                colaborador["senha"] = hashear_senha(senhas["nova"].get())
                editar_colaborador(colaborador)
                messagebox.showinfo(
                    title="Sucesso", message="Senha alterada com sucesso."
                )
                limpar()
            else:
                messagebox.showerror(
                    title="Senha fraca",
                    message="Insira uma senha mais forte, com pelo menos 8 caracteres.",
                )
                entry_nova_senha.delete("0", tk.END)
                entry_repita_senha.delete("0", tk.END)
                entry_nova_senha.focus()
        else:
            entry_nova_senha.delete("0", tk.END)
            entry_repita_senha.delete("0", tk.END)
            entry_nova_senha.focus()
            messagebox.showerror(
                title="Inválido",
                message="As senhas inseridas são diferentes.",
            )
    else:
        messagebox.showerror(
            title="Acesso negado.",
            message="Senha inválida.",
        )
        limpar()


def reconstruir_frame(colaborador):
    limpar_widgets()

    global frame_alterar_senha
    global senhas, entry_nova_senha, entry_repita_senha

    senhas = {}
    frame_alterar_senha = tk.Frame(contexto.frame_conteudo)

    frame_alterar_senha.grid(pady=200, padx=20)

    frame_alterar_senha.grid_rowconfigure(0, minsize=20, weight=1)
    frame_alterar_senha.rowconfigure((1, 2, 3, 4, 5, 6, 7), minsize=20)
    frame_alterar_senha.rowconfigure(8, minsize=250, weight=1)
    frame_alterar_senha.columnconfigure(0, minsize=10)
    frame_alterar_senha.columnconfigure(
        (1, 2, 3, 4, 5, 6, 7), pad=5, weight=1, minsize=2
    )
    frame_alterar_senha.grid(padx=0, pady=0)

    label_titulo = tk.Label(
        frame_alterar_senha,
        text="Alteração de Senha",
        font=(GUI_FONT, 22, "bold"),
    )

    # Senha atual
    label_senha_atual = tk.Label(
        frame_alterar_senha, text="Digite a senha atual: ", font=(GUI_FONT, 16, "bold")
    )
    campo_senha_atual = tk.StringVar()
    entry_senha_atual = tk.Entry(
        frame_alterar_senha,
        textvariable=campo_senha_atual,
        font=(GUI_FONT, 16),
        show="*",
    )
    entry_senha_atual.bind("<Return>", lambda event: salvar(event, colaborador))
    senhas["atual"] = campo_senha_atual

    ttk.Separator(contexto.frame_conteudo, orient="horizontal")

    # Nova senha
    label_nova_senha = tk.Label(
        frame_alterar_senha, text="Digite a nova senha: ", font=(GUI_FONT, 16, "bold")
    )
    campo_nova_senha = tk.StringVar()
    entry_nova_senha = tk.Entry(
        frame_alterar_senha,
        textvariable=campo_nova_senha,
        font=(GUI_FONT, 16),
        show="*",
    )
    entry_nova_senha.bind("<Return>", lambda event: salvar(event, colaborador))
    senhas["nova"] = campo_nova_senha

    # Repita senha
    label_repita_senha = tk.Label(
        frame_alterar_senha, text="Repita a nova senha: ", font=(GUI_FONT, 16, "bold")
    )
    campo_repita_senha = tk.StringVar()
    entry_repita_senha = tk.Entry(
        frame_alterar_senha,
        textvariable=campo_repita_senha,
        font=(GUI_FONT, 16),
        show="*",
    )
    entry_repita_senha.bind("<Return>", lambda event: salvar(event, colaborador))
    senhas["repita"] = campo_repita_senha

    # Botões
    botao_salvar = ttk.Button(
        frame_alterar_senha,
        text="Salvar",
        bootstyle="primary",
        command=lambda: salvar(None, colaborador),
    )
    botao_cancelar = ttk.Button(
        frame_alterar_senha,
        text="Cancelar",
        bootstyle="primary-outline",
        command=limpar,
    )

    # Row 1
    label_senha_atual.grid(row=1, column=0, pady=10, sticky="w")
    entry_senha_atual.grid(row=1, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 2
    label_nova_senha.grid(row=2, column=0, pady=10, sticky="w")
    entry_nova_senha.grid(row=2, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 3
    label_repita_senha.grid(row=3, column=0, pady=10, sticky="w")
    entry_repita_senha.grid(row=3, column=1, columnspan=2, ipadx=80, sticky="w")

    # Row 5
    botao_cancelar.grid(row=8, column=6, sticky="es", ipady=10, padx=2)
    botao_salvar.grid(row=8, column=7, sticky="wes", ipady=10, padx=2)


def alterar_senha_colaborador(colaborador: dict):
    return reconstruir_frame(colaborador)


if __name__ == "__main__":
    alterar_senha_colaborador()
