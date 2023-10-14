from pytube import YouTube
import os


music_dir = 'music'

# Create a folder to save the musics if this doen't exists.
def create_folder(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Download the youtube music
def download_from_yt(link: str) -> None:
    try:
        yt = YouTube(link)

        title = yt.title

        filename = f"{music_dir}/{title}.mp3"

        if os.path.exists(filename):
            print("File already exists")
            return

        video_stream = yt.streams.filter(only_audio=True).first()
        video_stream.download(filename=filename)
    except Exception as e:
        print(f"Error on link {link} : {e}")

create_folder(music_dir)

links = [
]

for i in range(len(links)):
    download_from_yt(links[i])