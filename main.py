# in the future allow for entering youtube playlist thus add Playlist from pytube
from pytube import YouTube 
import tkinter as tk 
from tkinter import messagebox, ttk
import requests
import threading

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

        self.thread = threading.Thread(target=self.start_download)

        # download button 
        self.download = tk.Button(self.master, text='Download', command=self.start_download)
        self.download.grid(row=4, column=0, padx=(10, 0), sticky='W', columnspan=2)

        # result section 
        self.result_label = tk.Label(self.master, text='Result: ')
        self.result_label.grid(row=5, column=0, sticky='W', padx=(25), pady=(10, 0))

    def start_download(self):
        self.thread.start()
        if len(self.link_entry.get()) == 0:
            messagebox.showerror(title='Invalid Link', message='Missing link.')
        token = self.authorization_entry.get()
        if len(token) == 0:
            messagebox.showerror(title='Invalid Token', message='Missing token.')
        headers = {'Authorization': 'Bearer ' + token}
        result = requests.get(self.link_entry.get(), headers=headers, params={'data': True}).json()
        if result is None:
            messagebox.showerror(title='Invalid Request', message='Invalid Link/Token was given; request rejected.')
        print(result.get('songs'))
        # show all the songs that are going to be downlodaed
        song_status = []
        row = 6
        for song in result.get('songs'):
            tk.Label(text=f"{song.get('title')} | {song.get('duration')}").grid(row=row, column=1)
            status_textvariable = tk.StringVar()
            status = tk.Label(textvariable=status_textvariable)
            status.grid(row=row, column=1)
            # TODO: fix this line here, going to only store the textvariabel in the array 
            song_status.append(status_textvariable)
            row+=1
        
        return 

        # reusing row as an index
        row = 0
        for song in result.get('songs'):
            video = YouTube('https://youtu.be/'+song.get('video_id'))
            # progressive = video/audio
            # filter progressive False to get video only
            # only_audio=True for only audio
            download = None
            if self.type_options.get() == 'Audio':
                download = video.streams.filter(only_audio=True).first()
            else:
                streams = video.streams.filter(progressive=True).order_by('resolution')
                option = self.quality_options.get()
                download = None
                if option == 'Low':
                    download = streams.first()
                elif option == 'Medium':
                    download = streams[len(streams)//2]
                elif option == 'High':
                    download = streams.last()
            # downloading into the a folder created using the title of the playlist
            download.download(result.get('title'))
            # update the status label
            song_status[row].set('Downloaded')
            row+=1 

        messagebox.showinfo(title='Downloaded Songs', message=f"Succesfully downloaded songs from the playlist: {result.get('title')}")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
