# in the future allow for entering youtube playlist thus add Playlist from pytube
from pytube import YouTube 
import tkinter as tk 
from tkinter import messagebox, ttk
import requests
import threading
from time import sleep

window = tk.Tk()
window.title('YuDo Downloader')
#window.grid_rowconfigure(0, weight=1)
#window.grid_columnconfigure(0, weight=1)
# link section
link_label = tk.Label(window, text='YuDo Link: ')
link_label.grid(row=0, column=0, padx=(50, 0), pady=(15, 0))
link_entry = tk.Entry(window)
link_entry.grid(row=0, column=1, pady=(15, 0), padx=(0, 50), sticky='W')

# authorization text 
authorization_label = tk.Label(window, text='Authorization Text: ')
authorization_label.grid(row=1, column=0, padx=(50, 0))
authorization_entry = tk.Entry(window) 
authorization_entry.grid(row=1, column=1)

type_label = tk.Label(window, text='Download Type: ')
type_label.grid(row=2, column=0, pady=(5, 0))
# video/audio or audio
type_options_variable = tk.StringVar()
type_options = ttk.Combobox(window, textvariable=type_options_variable)
type_options['values'] = ['Video/Audio', 'Audio']
type_options.current(0)
type_options.grid(row=3, column=0, padx=(10, 0))

quality_label = tk.Label(window, text='Download Quality: ')
quality_label.grid(row=2, column=1, pady=(5, 0))
# quality of the download
quality_options_variable = tk.StringVar()
quality_options = ttk.Combobox(window, textvariable=quality_options_variable)
quality_options['values'] = ['Low', 'Medium', 'High']
quality_options.current(0)
quality_options.grid(row=3, column=1, padx=(0, 10))

# result section 
result_label = tk.Label(window, text='Result: ')
result_label.grid(row=5, column=0, sticky='W', padx=(25), pady=(10, 0))


def start_download():
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

    for song in songs:
        print('this ran')
        video = YouTube('https://youtu.be/'+song.get('video_id'))
        # progressive = video/audio
        # filter progressive False to get video only
        # only_audio=True for only audio
        download = None
        if type_options.get() == 'Audio':
            download = video.streams.filter(only_audio=True).first()
        else:
            streams = video.streams.filter(progressive=True).order_by('resolution')
            option = quality_options.get()
            download = None
            if option == 'Low':
                download = streams.first()
            elif option == 'Medium':
                download = streams[len(streams)//2]
            elif option == 'High':
                download = streams.last()
        # downloading into the a folder created using the title of the playlist
        download.download(result.get('title'))

    song_status = []
    # show all the songs that are going to be downlodaed
    row = 6
    for song in songs:
        tk.Label(text=f"{song.get('title')} | {song.get('duration')}").grid(row=row, column=0)
        status_textvariable = tk.StringVar()
        status = tk.Label(textvariable=status_textvariable)
        status.grid(row=row, column=1)
        status_textvariable.set('Downloaded')
        song_status.append(status_textvariable)
        row+=1


    messagebox.showinfo(title='Downloaded Songs', message=f"Succesfully downloaded songs from the playlist: {result.get('title')}")

# download button 
download = tk.Button(window, text='Download', command=start_download)
download.grid(row=4, column=0, padx=(10, 0), sticky='W', columnspan=2)

window.mainloop()
