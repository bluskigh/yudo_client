# in the future allow for entering youtube playlist thus add Playlist from pytube
from pytube import YouTube 
import tkinter as tk 
from tkinter import messagebox, ttk
import requests

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

        self.type_label = tk.Label(self.master, text='Download Type: ')
        self.type_label.grid(row=1, column=0, pady=(5, 0))
        # video/audio or audio
        self.type_options_variable = tk.StringVar()
        self.type_options = ttk.Combobox(self.master, textvariable=self.type_options_variable)
        self.type_options['values'] = ['Video/Audio', 'Audio']
        self.type_options.current(0)
        self.type_options.grid(row=2, column=0, padx=(10, 0))

        self.quality_label = tk.Label(self.master, text='Download Quality: ')
        self.quality_label.grid(row=1, column=1, pady=(5, 0))
        # quality of the download
        self.quality_options_variable = tk.StringVar()
        self.quality_options = ttk.Combobox(self.master, textvariable=self.quality_options_variable)
        self.quality_options['values'] = ['Low', 'Medium', 'High']
        self.quality_options.current(0)
        self.quality_options.grid(row=2, column=1, padx=(0, 10))

        # download button 
        self.download = tk.Button(self.master, text='Download', command=self.start_download)
        self.download.grid(row=3, column=0, padx=(10, 0), sticky='W', columnspan=2)

        # result section 
        self.result_label = tk.Label(self.master, text='Result: ')
        self.result_label.grid(row=4, column=0, sticky='W', padx=(25), pady=(10, 0))

    def start_download(self):
        headers = {
                'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRQR21rd19RV3pGX0NzRXhkdFk4ViJ9.eyJpc3MiOiJodHRwczovL3J1c28udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYTQwNDg1NjlhYjBlMDA3MGE5ZjdiNSIsImF1ZCI6InJ1bm5lcnMiLCJpYXQiOjE2MjIyMzE1NjgsImV4cCI6MTYyMjIzODc2OCwiYXpwIjoibDA2cWVDMU1zMUpmNlVyUzdtM2JtYklZYmhwNkNuNkQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.JWBWfipw6nH5jvnfDUSX6RGQoHXdcArb6t1g3hlJMj1sBExSgtjUYnO988q-ZOpj103NjTpF1dboNRLqBo-n8e2YA-G4u7f0KmcKWOw9N2_qWbRvT6jfC1GvV1k9iq7XLn5IgZmZ7HF1LCDK4kTafu5Tfyn_LlhTj6wZ9FHe8YUb1h0LRnOgSHbQRlViKnDT4nbNUn77oYaWZxZ6DUhzl09I4d7qXH3PiZ5gmlFSHuqFiCMOWg41KjAa37YJsjfHIvHSckSI84FbyIk3iV7CYweiD1Sj0GrzOfbxCqFvzLjPcCj3EJnpODmME-PPjpYISMzzaFkNrS3mN8RxL57SKQ'
                }
        print(requests.get('http://127.0.0.1:5000/playlists/17', headers=headers, params={'data': True}).json())

root = tk.Tk()
app = Application(master=root)
app.mainloop()
