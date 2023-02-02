import re
import os

def upload_file():
    conf_file=open("discord-uploader.conf","r")
    conf=conf_file.readlines()
    directory=conf[2]
    directory=re.findall("\[([A-Za-z1-9_\-/]+)\]",directory)[0]
    contents=os.listdir(directory)
    conf_file.close()
    uploaded_files=open(".uploaded.txt","r")
    uploaded_file=uploaded_files.read().split(',')[:-1]
    not_uploaded=[]
    uploaded_files.close()
    uploaded_files=open(".uploaded.txt","a")
    for content in contents:
        if content not in uploaded_file:
            not_uploaded.append(content)
            uploaded_files.write(content)
            uploaded_files.write(',')
    uploaded_files.close()
    return not_uploaded