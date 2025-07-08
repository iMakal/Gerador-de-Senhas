import tkinter as tk
from tkinter import ttk  
from tkinter import messagebox
import random
import string

root = tk.Tk()
root.title('Gerador de Senhas')
root.iconbitmap("boticon.ico")


# Define tamanho fixo
largura_janela = 600
altura_janela = 600
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

# Estilo da barra de força
style = ttk.Style()
style.theme_use('clam')

style.configure("red.Horizontal.TProgressbar", troughcolor='gray', background='red')
style.configure("yellow.Horizontal.TProgressbar", troughcolor='gray', background='yellow')
style.configure("green.Horizontal.TProgressbar", troughcolor='gray', background='green')
style.configure("blue.Horizontal.TProgressbar", troughcolor='gray', background='blue')



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

    # Atualiza barra de força e texto
    forca_texto, pontuacao = avaliar_forca_senha(senha)
    atualizar_barra_forca(forca_texto, pontuacao)
    barra_forca["value"] = pontuacao
    label_forca["text"] = f"Força da senha: {forca_texto}"



def avaliar_forca_senha(senha):
    pontuacao = 0
    comprimento = len(senha)

    # Presença dos tipos de caracteres
    upper_case = any(c.isupper() for c in senha)
    lower_case = any(c.islower() for c in senha)
    special = any(c in string.punctuation for c in senha)
    digit = any(c.isdigit() for c in senha)

    # Contar caracteres repetidos consecutivos
    repetidos = 0
    for i in range(1, comprimento):
        if senha[i] == senha[i-1]:
            repetidos += 1

    # Avaliação de comprimento
    if comprimento >= 8:
        pontuacao += 1
    if comprimento >= 12:
        pontuacao += 1
    if comprimento >= 16:
        pontuacao += 2  # mais peso para senhas mais longas

    # Diversidade de caracteres
    tipos = sum([upper_case, lower_case, digit, special])
    pontuacao += tipos * 2  # peso maior para variedade

    # Penaliza repetições consecutivas
    if repetidos > 0:
        pontuacao -= repetidos  # diminui pontuação para repetições

    # Limita pontuação mínima a 0
    pontuacao = max(pontuacao, 0)

    # Avaliação final
    if pontuacao <= 3:
        return "Fraca", pontuacao
    elif pontuacao <= 5:
        return "Moderada", pontuacao
    elif pontuacao <= 8:
        return "Forte", pontuacao
    else:
        return "Muito Forte", pontuacao
    

def atualizar_barra_forca(forca_texto, pontuacao):
    barra_forca["value"] = pontuacao
    label_forca["text"] = f"Força da senha: {forca_texto}"

    if forca_texto == "Fraca":
        barra_forca.configure(style="red.Horizontal.TProgressbar")
    elif forca_texto == "Moderada":  # alinhado com o retorno da avaliação
        barra_forca.configure(style="yellow.Horizontal.TProgressbar")
    elif forca_texto == "Forte":
        barra_forca.configure(style="green.Horizontal.TProgressbar")
    else:  # Muito Forte
        barra_forca.configure(style="blue.Horizontal.TProgressbar")


# Label mensagens
mensagem_var = tk.StringVar()
mensagem_label = tk.Label(root, textvariable=mensagem_var, fg="green")
mensagem_label.grid(row=6, column=0, columnspan=2, pady=(0,20))

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

# Label força da senha
label_forca = tk.Label(root, text="Força da senha:", width=25, anchor="w")
barra_forca = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate", maximum=10)
label_forca.grid(row=4, column=0, sticky="w", padx=20, pady=(15, 0))
barra_forca.grid(row=4, column=1, padx=20, pady=(15, 20), sticky="ew")


# Botões lado a lado
btn_gerar = tk.Button(root, text="Gerar Senha", command=gerar_senha)
btn_copiar = tk.Button(root, text="Copiar senha", command=copiar_para_clipboard)

btn_gerar.grid(row=5, column=0, pady=20, padx=(20,10), sticky="ew")
btn_copiar.grid(row=5, column=1, pady=20, padx=(10,20), sticky="ew")

# Configura colunas para expandir
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
