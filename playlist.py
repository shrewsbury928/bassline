import pygame.mixer as mixer
from song import Song
import random as r

class Playlist():
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.cover = "images/Placeholder_Song.png"  # Default cover
        self.songs = []
        self.run_length = "0m 0s"
        self.stopped = True

    def add_song(self, song):
        self.songs.append(song)

    #shuffle button
    def shuffle(self):
        r.shuffle(self.songs)

    #play button
    def listen(self):
        curr_index = 0

        self.songs[curr_index].audio.play()
        self.stopped = False
        
        #queue tracker
        while not self.stopped:            
            current = self.songs[curr_index].audio
            if curr_index+1 < len(self.songs):
                nxt = self.songs[curr_index+1].audio
            else:
                nxt = self.songs[0].audio

            if not mixer.music.get_busy() or self.stopped:
                mixer.play(nxt)

            curr_index += 1   
            
             
    def stop(self):
        mixer.stop()
        self.stopped = True

    #description set - save button
    def set_description(self, desc):
        self.description = desc

    #calculates length in mins + secs
    def get_length(self):
        total = 0.0
        #for i in range(len(self.songs)):
        #    total+= self.songs[i].tags.duration
        self.run_length = f"{total//60}m {total%60}s"

    #saves updates
    def save(self, desc=""):
        self.get_length()
        if desc:
            self.set_description(desc)