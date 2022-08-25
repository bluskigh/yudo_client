### YuDo Client
Assists in downloading playlists that are created in web application 'YuDo'.
## Requirements
Install Python3 on your machine (https://www.python.org/downloads/)

Install the needed packages by running:
```
pip3 install -r requirements.txt
```

It is probable that you have tkinter installed; however, if you see the ensuing error when attempting to run the program "ModuleNotFoundError: No module named 'tkinter' in python." Then run the following statement in your terminal:
''' 
sudo apt install python3-tkinter
'''
## Running
To start the application run:
```
python3 main.py
```
## Errors
### PyTube
Usually if the application is operating incorrectly it is because of the utilization of a deprecated version of PyTube. So to fix this issue run this command:
'''
pip3 install --upgrade pytube
'''
I will try to update the the requirements.txt to fit recent releases.
