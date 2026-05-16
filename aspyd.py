import yt_dlp
import rich

print("aspyd - a simple python youtube downloader")
print("1. download a video")
print("2. download an audio")
print("3. download a playlist")
selection = input("select an option: ")

if selection == "1":
    url = input("enter url: ")
    with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
        ydl.download([url])
    v_id = input("enter video ID: ").strip()
    a_id = input("enter audio ID: ").strip()
    
    save_directory = input("where do you wanna save the file? (type for . for current directory): ")
    vid_opt = {
        'paths': {'home': save_directory},
        'format': f'{v_id}+{a_id}', 
        'outtmpl': '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(vid_opt) as ydl:
        ydl.download([url])

elif selection == "2":
    url = input("enter url: ")
    audio_codec = input("enter audio codec (mp3, m4a, opus, vorbis, flac, wav): ")
    save_directory = input("where do you wanna save the file? (type for . for current directory): ")
    aud_opt = {
        'paths': {'home': save_directory},
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

elif selection == "3":
    url = input("enter url: ")
    res = input("enter max resolution (eg: 1080, 720): ")
    codec = input("enter video codec ('avc1' (H.264 mp4), 'vp9' (webM), 'av01' (AV1 webM): ")
    save_directory = input("where do you wanna save the file? (type for . for current directory): ")

    pl_opt = {
        'paths': {'home': save_directory},
        'format': f'bestvideo[vcodec^={codec}][height<={res}]+bestaudio/best[height<={res}]',
        'merge_output_format': 'mp4' if codec == 'avc1' else 'webm',
        'noplaylist': False,
        'extract_flat': False,
        'outtmpl': '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
        'ignoreerrors': True,
        'retries': 10,     
        'fragment_retries': 10, 
        'file_access_retries': 3,
    }

    with yt_dlp.YoutubeDL(pl_opt) as ydl:
        ydl.download([url])
    

else:
    print(f'{selection} is not an option')