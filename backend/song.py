import TinyTag
import pygame.mixer as mixer
#import songs
mixer.init()

class Song():
    def __init__(self, mp3_path, img_path, genre: str):
        self.audio = mixer.Sound(mp3_path)

        if img_path == None:
            img_path = r"blank.png"
        self.cover = open(img_path, 'r')
        tags = TinyTag.get(mp3_path)
        self.token = genre
        self.playing = False

    def play(self):
        self.audio.play()
        self.playing = True

    def un_pause(self):
        if self.playing == True:
            mixer.pause()
            print("paused")
            self.playing = False
        else:
            mixer.unpause()
            print("unpaused")
            self.playing = True
            
    def stop(self):
        mixer.stop()
        self.playing = False

song = Song(r'songs\test_song.mp3',None,"pop" )


'''
test = '5'
while test != '0':
    test = input("2 = pause/resume, 0 = stop, 1 = play: ")

    match test:
        case '1':
            song.play()
            print("playing")
        case '2':
            song.un_pause()
        case '0':
            break
        case _:
            pass
    test = '5'

song.stop()
'''