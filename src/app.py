import tkinter as tk
from tkinter import ttk
import os
from pytube import YouTube
import threading

TITLE = "Jeff YT Music Downloader"
MUSIC_DIR = os.path.join(os.path.expanduser('~'), 'Music')

# Função para transformar o título da música em um título válido
def transform_title(title: str) -> str:
    text = title.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    return text[:40]

# Função para iniciar o download
def download_music():
    global download_thread
    if 'download_thread' in globals() and download_thread.is_alive():
        print("Download is already in progress.")
        return

    global link
    link = input.get()

    download_thread = threading.Thread(target=download_thread_function)
    download_thread.start()

# Função para baixar o vídeo em uma thread separada
def download_thread_function():
    update_status_label("Downloading...")
    try:
        yt = YouTube(link)
        title = transform_title(yt.title)
        filename = os.path.join(MUSIC_DIR, f"{title}.mp3")

        if os.path.exists(filename):
            update_status_label("File already exists")
            return

        video_stream = yt.streams.filter(only_audio=True).first()
        video_stream.download(filename=filename)

        update_status_label("Download completed.")
    except Exception as e:
        message = f"Error on link {link}: {e}"
        update_status_label(message)
        print(message)

    clear_input()

# Função para atualizar o rótulo de status
def update_status_label(text: str):
    status_label.config(text=text)

# Função para limpar a entrada de URL
def clear_input():
    input.delete(0, tk.END)

# Função para limpar o rótulo de status
def clear_status_label():
    update_status_label("Status: ")

# Função para limpar a entrada e o rótulo de status
def clear_all():
    clear_input()
    clear_status_label()

def open_music_dir():
    os.startfile(MUSIC_DIR)

# Crie a janela
window = tk.Tk()
window.title(TITLE)
window.geometry("500x250")
window.resizable(False, False)
window.iconphoto(False, tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'icon.png')))

# Crie o rótulo
label = tk.Label(window, text="URL do vídeo:", font=("Helvetica", 12))
label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Crie a entrada de URL
input = tk.Entry(window, width=40)
input.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Crie o botão de download
button = tk.Button(window, text="Download", command=download_music, bg="green", fg="white")
button.grid(row=0, column=2, padx=10, pady=10)

# Crie o rótulo de status
status_label = tk.Label(window, text="Status: ", font=("Helvetica", 12))
status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Crie o botão Limpar
clear_button = tk.Button(window, text="Limpar", command=clear_all, bg="red", fg="white")
clear_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Crie o rótulo para o diretório de música
music_dir_label = tk.Label(window, text=f"Músicas serão baixadas em: {MUSIC_DIR}", font=("Helvetica", 10))
music_dir_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

open_music_dir_button = tk.Button(window, text="Abrir pasta", command=open_music_dir)
open_music_dir_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Inicie a janela
window.mainloop()
