from pytube import YouTube
import tkinter as tk
from tkinter import ttk
import os
from moviepy.editor import VideoFileClip
import threading

TITLE = "Jeff YT Music Downloader"
MUSIC_DIR=os.path.join(os.path.expanduser('~'), 'Music')

# Function to transform the music invalid title in a valid title
def transform_title(title: str) -> str:
    text = title.replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    return text[:40]

# Function to initiate the download
def download_music():
    global download_thread  # Define a global variable to hold the download thread
    if 'download_thread' in globals() and download_thread.is_alive():
        print("Download is already in progress.")
        return

    global link
    link = input.get()

    download_thread = threading.Thread(target=download_thread_function)
    download_thread.start()

# Function to download the video in a separate thread
def download_thread_function():
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
        message = f"Error on link {link} : {e}"
        update_status_label(message)
        print(message)

    clear_input()

# Função para atualizar o rótulo de status
def update_status_label(text: str):
    status_label.config(text=text)

# Função para atualizar a barra de progresso
def update_progress_bar(value: int):
    progress_bar['value'] = value

# Função para limpar a entrada de URL
def clear_input():
    input.delete(0, tk.END)

# Função para limpar o rótulo de status
def clear_status_label():
    update_status_label("Status: ")

# Função para limpar a barra de progresso
def clear_progress_bar():
    update_progress_bar(0)

# Função para limpar a entrada, rótulo de status e barra de progresso
def clear_all():
    clear_input()
    clear_status_label()
    clear_progress_bar()

# Crie a janela
window = tk.Tk()
window.title(TITLE)
window.geometry("500x200")
window.resizable(False, False)

# Crie o rótulo
label = tk.Label(window, text="URL do vídeo:")
label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Crie a entrada de URL
input = tk.Entry(window, width=40)
input.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Crie o botão de download
button = tk.Button(window, text="Download", command=download_music, bg='green', fg='white')
button.grid(row=0, column=2, padx=10, pady=10)

# Crie o rótulo de status
status_label = tk.Label(window, text="Status: ", font=("Helvetica", 12))
status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Crie a barra de progresso
progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=400, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Crie o botão Limpar
clear_button = tk.Button(window, text="Limpar", command=clear_all, bg='red', fg='white')
clear_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Inicie a janela
window.mainloop()
