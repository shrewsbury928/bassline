from tinytag import TinyTag as tag
import pygame.mixer as mixer
import pickle
mixer.init()

class Song():
    def __init__(self, mp3_path, genre: str = 'n/a'):
        self.path = mp3_path
        tags: tag = tag.get(self.path, image=True)
        images = tags.images
        self.cover = images.front_cover
        if self.cover == None:
            self.cover = r"one.png"
        tags = tag.get(mp3_path)
        self.token = tags.genre
        self.paused = True

    def store(self):
        pass
