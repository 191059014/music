import json
import os
filenames = os.listdir("D:\\Program Files\\KuGou")
songs = []
for filename in filenames:
    if filename.endswith('.mp3'):
        songs.append({'name':filename[:-4], 'url':filename})
print(songs)