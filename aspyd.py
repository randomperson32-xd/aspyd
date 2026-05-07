import yt_dlp

print("aspyd - a simple python youtube downloader")
url = input("video url: ")

with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
    ydl.download([url])

v_id = input("Enter Video ID: ").strip()
a_id = input("Enter Audio ID: ").strip()

download_opts = {
    'format': f'{v_id}+{a_id}', 
    'outtmpl': '%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(download_opts) as ydl:
    ydl.download([url])