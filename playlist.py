import pygame.mixer as mixer
from song import Song
import random as r

class Playlist():
    def __init__(self, title, desc = ''):
        self.title = title
        self.description = desc
        self.cover = "one.png"
        self.songs = []
        self.queue = []
        self.run_length = "0m 0s"
        self.curr_index = 0
        self.stopped = True

    def add_song(self, song):
        self.songs.append(song)

    #shuffle button
    def shuffle(self):
        self.queue = self.songs
        shuffle = r.shuffle(self.queue)
        self.queue = shuffle

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
    def save(self, desc = ''):
        self.get_length()
        self.set_description(desc)
        self.queue = self.songs

    def view(self):
        print(self.title, self.description, self.run_length)
        for song in self.songs:
            print(song.token)
    
    def listen(self):
        pass

# P = Playlist("test")
# a = Song(r'C:/Users/s-khatri19/OneDrive - st-bernards.slough.sch.uk/A level comp-sci/CO3 - NEA/Bassline/bassline/library/test_song.mp3', None, "lofi")
# b = Song(r'C:/Users/s-khatri19/OneDrive - st-bernards.slough.sch.uk/A level comp-sci/CO3 - NEA/Bassline/bassline/library/test_song.mp3', None, "pop")
# c = Song(r'C:/Users/s-khatri19/OneDrive - st-bernards.slough.sch.uk/A level comp-sci/CO3 - NEA/Bassline/bassline/library/test_song.mp3', None, "rock")


# P.add_song(a)
# P.add_song(b)
# P.add_song(c)
# P.save('1')
# #P.listen()
# P.view()

    
