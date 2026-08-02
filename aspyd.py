import yt_dlp
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

console.print(Panel("[bold cyan]aspyd - a simple python youtube downloader[/bold cyan]", expand=False))
print("1. download a video")
print("2. download an audio")
print("3. download a playlist")
selection = input("select an option: ")

def create_progress_hook():
    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    )
    task_id = None
    
    def hook(d):
        nonlocal task_id
        if d['status'] == 'downloading':
            if task_id is None:
                progress.start()
                filename = d.get('filename', 'downloading').split('/')[-1]
                if len(filename) > 30:
                    filename = filename[:27] + "..."
                task_id = progress.add_task(filename, total=100)
            
            try:
                clean_pct = ''.join(c for c in d.get('_percent_str', '0') if c.isdigit() or c == '.')
                pct = float(clean_pct) if clean_pct else 0.0
                progress.update(task_id, completed=pct)
            except ValueError:
                pass
                
        elif d['status'] == 'finished':
            if task_id is not None:
                progress.update(task_id, completed=100)
                progress.stop()
                console.print("[bold green]✓ download complete![/bold green]")
                
    return hook

base_hooks = {'progress_hooks': [create_progress_hook()]}

try:
    if selection == "1":
        url = input("enter url: ")
        with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
            ydl.download([url])
        v_id = input("enter video ID: ").strip()
        a_id = input("enter audio ID: ").strip()
        
        save_directory = input("where do you wanna save the file? (type . for current directory): ")
        vid_opt = {
            **base_hooks,
            'paths': {'home': save_directory},
            'format': f'{v_id}+{a_id}', 
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(vid_opt) as ydl:
            ydl.download([url])

    elif selection == "2":
        url = input("enter url: ")
        audio_codec = input("enter audio codec (mp3, m4a, opus, vorbis, flac, wav): ")
        save_directory = input("where do you wanna save the file? (type . for current directory): ")
        aud_opt = {
            **base_hooks,
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
        save_directory = input("where do you wanna save the file? (type . for current directory): ")

        pl_opt = {
            **base_hooks,
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
        console.print(f'[bold red]{selection} is not an option[/bold red]')

except yt_dlp.utils.DownloadError:
    console.print("\n[bold red]✕ download failed [/bold red]")
except KeyboardInterrupt:
    console.print("\n[bold yellow]! operation cancelled [/bold yellow]")
except Exception as e:
    console.print(f"\n[bold red]✕ an error occurred:[/bold red] {e}")

    