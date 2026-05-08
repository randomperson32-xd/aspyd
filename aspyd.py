import yt_dlp

print("aspyd - a simple python youtube downloader")
print("1. download a video")
print("2. download an audio")
selection = input("select an option: ")

if selection == "1":
    url = input("video url: ")
    with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
        ydl.download([url])
    v_id = input("enter video ID: ").strip()
    a_id = input("enter audio ID: ").strip()
    vid_opt = {
        'format': f'{v_id}+{a_id}', 
        'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(vid_opt) as ydl:
        ydl.download([url])

elif selection == "2":
    url = input("video url: ")
    audio_codec = input("enter audio codec (mp3, m4a, opus, vorbis, flac, wav): ")

    aud_opt = {
        'format': 'bestaudio/best',
        'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_codec,
                'preferredquality': '192',
            },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ],
    }

    with yt_dlp.YoutubeDL(aud_opt) as ydl:
        ydl.download([url])

else:
    print(f'{selection} is not an option')