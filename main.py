# in the future allow for entering youtube playlist thus add Playlist from pytube
from os import listdir, getcwd
from time import sleep
import re
import threading
import requests
from pytube import YouTube 
import tkinter as tk
from tkinter import messagebox, ttk, font

window = tk.Tk()
window.title('YuDo Downloader')
#window.grid_rowconfigure(0, weight=1)
#window.grid_columnconfigure(0, weight=1)
# link section
font = ('Noto Sans Display', '15', 'bold')
font_medium = ('Noto Sans Display', '13', 'bold')
font_entry = ('Noto Sans Display', '13')

link_label = tk.Label(window, font=font, text='YuDo Link: ')
link_label.grid(row=0, column=0, padx=(50, 0), pady=(15, 0))
link_entry = tk.Entry(window, font=font_entry)
link_entry.grid(row=0, column=1, pady=(15, 0), padx=(0, 50), sticky='W')

# authorization text 
authorization_label = tk.Label(window, font=font, text='Authorization Text: ')
authorization_label.grid(row=1, column=0, padx=(50, 0))
authorization_entry = tk.Entry(window, font=font_entry) 
authorization_entry.grid(row=1, column=1)

type_label = tk.Label(window, font=font_medium, text='Download Type: ')
type_label.grid(row=2, column=0, pady=(5, 0))
# video/audio or audio
type_options_variable = tk.StringVar()
type_options = ttk.Combobox(window, font=font_entry, textvariable=type_options_variable)
type_options['values'] = ['Video/Audio', 'Audio']
type_options.current(0)
type_options.grid(row=3, column=0, padx=(10, 0))

quality_label = tk.Label(window, font=font_medium, text='Download Quality: ')
quality_label.grid(row=2, column=1, pady=(5, 0))
# quality of the download
quality_options_variable = tk.StringVar()
quality_options = ttk.Combobox(window, font=font_entry, textvariable=quality_options_variable)
quality_options['values'] = ['Low', 'Medium', 'High']
quality_options.current(0)
quality_options.grid(row=3, column=1, padx=(0, 10))

# result section 
result_label = tk.Label(window, font=('Noto Sans Display', '10', 'bold'), text='Result: ')
result_label.grid(row=5, column=0, sticky='W', padx=(25), pady=(10, 0))

process_variable = tk.StringVar()
process_label = tk.Label(window, font=('Noto Sans Display', '10'), textvariable=process_variable)
process_label.grid(row=5, column=1)

song_status = []

def safe_filename(s, max_length = 255):
    """credit: https://github.com/pytube/pytube/blob/master/pytube/helpers.py"""
    # Characters in range 0-31 (0x00-0x1F) are not allowed in ntfs filenames.
    ntfs_characters = [chr(i) for i in range(0, 31)]
    characters = [
        r'"',
        r"\#",
        r"\$",
        r"\%",
        r"'",
        r"\*",
        r"\,",
        r"\.",
        r"\/",
        r"\:",
        r'"',
        r"\;",
        r"\<",
        r"\>",
        r"\?",
        r"\\",
        r"\^",
        r"\|",
        r"\~",
        r"\\\\",
    ]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    filename = regex.sub("", s)
    return filename[:max_length].rsplit(" ", 0)[0] + '.mp4'

def start_download():
    process_variable.set('Downloading...')
    if len(link_entry.get()) == 0:
        messagebox.showerror(title='Invalid Link', message='Missing link.')
        return
    token = authorization_entry.get()
    if len(token) == 0:
        messagebox.showerror(title='Invalid Token', message='Missing token.')
        return
    headers = {'Authorization': 'Bearer ' + token}
    try:
        result = requests.get(link_entry.get(), headers=headers, params={'data': True}).json()
    except Exception as e:
        messagebox.showerror(title='Invalid Request', message='Configure the inputs, and try again.')
        return

    songs = result.get('songs')
    # attempting to get all existing songs that have downloaded
    existing_songs = []
    try:
        existing_songs = listdir(getcwd()+f'/{result.get("title")}')
        print(existing_songs)
    except FileNotFoundError:
        print('Folder not found')
        # playlist has not been downloaded to users computer
        pass
    row = 6
    # reusing row as an index
    for song in songs:
        download = None
        status_textvariable = tk.StringVar()
        temp = tk.Label(font=('Noto Sans Display', '13'), text=f"{song.get('title')} | {song.get('duration')}")
        status = tk.Label(font=font_medium, textvariable=status_textvariable)
        temp.grid(row=row, column=0)
        status.grid(row=row, column=1)
        if safe_filename(song.get('title')) in existing_songs:
            print('Already downloaded, ', song.get('title'))
            status_textvariable.set('Already Downloaded')
        else:
            try: 
                video = YouTube('https://youtu.be/'+song.get('video_id'))
                print(f'Going to download {video.title}')
            except:
                # video is unavailable now
                continue
            # progressive = video/audio
            # filter progressive False to get video only
            # only_audio=True for only audio
            if type_options.get() == 'Audio':
                download = video.streams.filter(only_audio=True).first()
            else:
                streams = video.streams.filter(progressive=True).order_by('resolution')
                option = quality_options.get()
                if option == 'Low':
                    download = streams.first()
                elif option == 'Medium':
                    download = streams[len(streams)//2]
                elif option == 'High':
                    download = streams.last()
            # downloading into the a folder created using the title of the playlist
            download.download(result.get('title'))
            status_textvariable.set('Downloaded')
        song_status.append([temp, status, status_textvariable])
        row+=1
    print('done')

# download button 
download = tk.Button(window, text='Download', command=start_download)
download.grid(row=4, column=0, padx=(22, 0), pady=(5, 0), sticky='W', columnspan=2)

window.mainloop()
