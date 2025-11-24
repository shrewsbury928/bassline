#import TinyTags
import pygame.mixer as mixer
mixer.init()

class Song():
    def __init__(self, mp3_path, img_path = r'library\one.png', genre =''):
        self.audio = mixer.Sound(mp3_path)

        self.cover = open(img_path, 'r')
        #tags = TinyTags.get(mp3_path)
        self.token = genre
        self.paused = True

    def play(self):
        self.audio.play()
        self.paused = False

    def un_pause(self):
        if self.paused == False:
            mixer.pause()
            self.paused = True
        else:
            mixer.unpause()
            self.paused = False
            
##
##song = Song("test_song.mp3",'one.png',"pop" )
##
##test = '5'
##while test != '0':
##    test = input("2 = pause/resume, 0 = stop, 1 = play: ")
##
##    match test:
##        case '1':
##            song.play()
##            print("playing")
##        case '2':
##            song.un_pause()
##        case '0':
##            mixer.stop()
##            break
##        case _:
##            pass
##    test = '5'

