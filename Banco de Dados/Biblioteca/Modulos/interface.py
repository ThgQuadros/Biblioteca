import tkinter as tk

# Instancia a janela principal
janela = tk.Tk()
janela.title("Minha Primeira Interface")
janela.geometry("300x200")

# Adiciona um texto simples (Label)
texto = tk.Label(janela, text="Olá, Tkinter!")
texto.pack(pady=50)

# Inicia o loop da janela
janela.mainloop()