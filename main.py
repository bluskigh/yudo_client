# in the future allow for entering youtube playlist thus add Playlist from pytube
from pytube import YouTube 
import tkinter as tk 
from tkinter import messagebox, ttk 
import requests
import threading
from time import sleep

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('YuDo Downloader')
        self.create_widgets()
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
    def create_widgets(self):
        # link section
        self.link_label = tk.Label(self.master, text='YuDo Link: ')
        self.link_label.grid(row=0, column=0, padx=(50, 0), pady=(15, 0))
        self.link_entry = tk.Entry(self.master)
        self.link_entry.grid(row=0, column=1, pady=(15, 0), padx=(0, 50), sticky='W')

        # authorization text 
        self.authorization_label = tk.Label(self.master, text='Authorization Text: ')
        self.authorization_label.grid(row=1, column=0, padx=(50, 0))
        self.authorization_entry = tk.Entry(self.master)
        self.authorization_entry.grid(row=1, column=1)

        self.type_label = tk.Label(self.master, text='Download Type: ')
        self.type_label.grid(row=2, column=0, pady=(5, 0))
        # video/audio or audio
        self.type_options_variable = tk.StringVar()
        self.type_options = ttk.Combobox(self.master, textvariable=self.type_options_variable)
        self.type_options['values'] = ['Video/Audio', 'Audio']
        self.type_options.current(0)
        self.type_options.grid(row=3, column=0, padx=(10, 0))

        self.quality_label = tk.Label(self.master, text='Download Quality: ')
        self.quality_label.grid(row=2, column=1, pady=(5, 0))
        # quality of the download
        self.quality_options_variable = tk.StringVar()
        self.quality_options = ttk.Combobox(self.master, textvariable=self.quality_options_variable)
        self.quality_options['values'] = ['Low', 'Medium', 'High']
        self.quality_options.current(0)
        self.quality_options.grid(row=3, column=1, padx=(0, 10))

        # download button 
        self.download = tk.Button(self.master, text='Download', command=self.start_download)
        self.download.grid(row=4, column=0, padx=(10, 0), sticky='W', columnspan=2)

        # result section 
        self.result_label = tk.Label(self.master, text='Result: ')
        self.result_label.grid(row=5, column=0, sticky='W', padx=(25), pady=(10, 0))

        self.song_status = []

    def start_download(self):
        row = 0
        for song in self.song_status:
            song[0].destroy()
            song[1].destroy()
            del song[2]
            song.pop(row)
            row += 1

        if len(self.link_entry.get()) == 0:
            messagebox.showerror(title='Invalid Link', message='Missing link.')
        token = self.authorization_entry.get()
        if len(token) == 0:
            messagebox.showerror(title='Invalid Token', message='Missing token.')
        headers = {'Authorization': 'Bearer ' + token}
        result = requests.get(self.link_entry.get(), headers=headers, params={'data': True}).json()
        if result is None:
            messagebox.showerror(title='Invalid Request', message='Invalid Link/Token was given; request rejected.')

        songs = result.get('songs')
        # show all the songs that are going to be downlodaed

        max_tries = 25 
        tries = 0
        row = 6
        # reusing row as an index
        for song in songs:
            download = None
            try:
                video = YouTube('https://www.youtu.be/'+song.get('video_id'))
                temp = tk.Label(text=f"{song.get('title')} | {song.get('duration')}")
                temp.grid(row=row, column=0)
                status_textvariable = tk.StringVar()
                status = tk.Label(textvariable=status_textvariable)
                status.grid(row=row, column=1)
                # progressive = video/audio
                # filter progressive False to get video only
                # only_audio=True for only audio
                if self.type_options.get() == 'Audio':
                    download = video.streams.filter(only_audio=True).first()
                else:
                    streams = video.streams.filter(progressive=True).order_by('resolution')
                    option = self.quality_options.get()
                    if option == 'Low':
                        download = streams.first()
                    elif option == 'Medium':
                        download = streams[len(streams)//2]
                    elif option == 'High':
                        download = streams.last()
                # downloading into the a folder created using the title of the playlist
                download.download(result.get('title'))
                status_textvariable.set('Downloaded')
            except Exception as e:
                print(f"Failed to download, attempting again.")
                try:
                    video = YouTube('https://youtu.be/'+song.get('video_id'))
                    video.streams.filter(only_audio=True).first().download(result.get('title'))
                    status_textvariable.set('Downloaded')
                except:
                    status_textvariable.set('Could Not Download')
            self.song_status.append([temp, status, status_textvariable])
            row+=1
        messagebox.showinfo(title='Downloaded Songs', message=f"Succesfully downloaded songs from the playlist: {result.get('title')}")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
