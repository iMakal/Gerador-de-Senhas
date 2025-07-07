import tkinter as tk
from tkinter import messagebox
import random
import string

root = tk.Tk()
root.title('Gerador de Senhas')
root.iconbitmap("boticon.ico")


# Define tamanho fixo
largura_janela = 500
altura_janela = 300
root.minsize(largura_janela, altura_janela)
root.resizable(False, False)

# Centraliza a janela no ecrã
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

# Variáveis
resultado_var = tk.StringVar()
incluir_maiusculas = tk.BooleanVar()
incluir_minusculas = tk.BooleanVar()
incluir_numeros = tk.BooleanVar()
incluir_especiais = tk.BooleanVar()
comprimento_var = tk.IntVar(value=12)

# Funções
def gerar_senha():
    caracteres_possiveis = ""
    if incluir_maiusculas.get():
        caracteres_possiveis += string.ascii_uppercase
    if incluir_minusculas.get():
        caracteres_possiveis += string.ascii_lowercase
    if incluir_numeros.get():
        caracteres_possiveis += string.digits
    if incluir_especiais.get():
        caracteres_possiveis += string.punctuation

    if caracteres_possiveis == "":
        messagebox.showerror("Erro", "Selecione pelo menos um tipo de caractere.")
        return

    comprimento = comprimento_var.get()
    if comprimento < 4 or comprimento > 32:
        messagebox.showerror("Erro", "O comprimento deve estar entre 4 e 32.")
        return

    senha = ''.join(random.choices(caracteres_possiveis, k=comprimento))
    resultado_var.set(senha)

# Label para mensagens
mensagem_var = tk.StringVar()
mensagem_label = tk.Label(root, textvariable=mensagem_var, fg="green")
mensagem_label.grid(row=5, column=0, columnspan=2, pady=(0,20))

def copiar_para_clipboard():
    senha = resultado_var.get()
    if not senha:
        messagebox.showwarning("Aviso","Nenhuma senha para copiar")
        return
    root.clipboard_clear()
    root.clipboard_append(senha)
    mensagem_var.set("Senha copiada com sucesso!")
    # Apaga a mensagem após 3 segundos
    root.after(3000, lambda: mensagem_var.set(""))

# Layout usando grid

# Label para o resultado
tk.Label(root, text="Senha gerada:").grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

# Entry readonly para mostrar senha
resultado_entry = tk.Entry(root, textvariable=resultado_var, font=("Consolas", 14), state="readonly")
resultado_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20)

# Frame para checkboxes
frame_opcoes = tk.Frame(root)
frame_opcoes.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

# Checkbuttons (organizados em grid dentro do frame)
tk.Checkbutton(frame_opcoes, text="Incluir letras maiúsculas", variable=incluir_maiusculas).grid(row=0, column=0, sticky="w")
tk.Checkbutton(frame_opcoes, text="Incluir letras minúsculas", variable=incluir_minusculas).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_opcoes, text="Incluir números", variable=incluir_numeros).grid(row=0, column=1, sticky="w", padx=20)
tk.Checkbutton(frame_opcoes, text="Incluir caracteres especiais", variable=incluir_especiais).grid(row=1, column=1, sticky="w", padx=20)

# Frame para comprimento e rótulos
frame_comprimento = tk.Frame(root)
frame_comprimento.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

tk.Label(frame_comprimento, text="Comprimento da senha:").pack(side="left")
tk.Spinbox(frame_comprimento, from_=4, to=32, textvariable=comprimento_var, width=5, state="readonly").pack(side="left", padx=5)
tk.Label(frame_comprimento, text="(Min: 4 Max: 32)").pack(side="left")

# Botões lado a lado
btn_gerar = tk.Button(root, text="Gerar Senha", command=gerar_senha)
btn_copiar = tk.Button(root, text="Copiar senha", command=copiar_para_clipboard)

btn_gerar.grid(row=4, column=0, pady=20, padx=(20,10), sticky="ew")
btn_copiar.grid(row=4, column=1, pady=20, padx=(10,20), sticky="ew")

# Configura colunas para expandir
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
