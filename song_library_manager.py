import os
from song import Song
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class SongLibraryManager:
    #loads and manages all songs#

    def __init__(self, songs_folder="library"):
        self.songs_folder = songs_folder
        self.all_songs = []
        self.__isLoaded = False

    def load_songs(self, force_reload=False):
        #is already loaded: return existing list
        if self.__isLoaded and not force_reload:
            return self.all_songs

        #file path does not exist: make new folder
        if not os.path.exists(self.songs_folder):
            os.makedirs(self.songs_folder)
            return self.all_songs

        #load all songs from folder
        for filename in os.listdir(self.songs_folder):
            #check for valid audio file extensions
            if filename.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                file_path = os.path.join(self.songs_folder, filename)
                #attempt to create Song object and add to list
                try:
                    song = Song(file_path)
                    self.all_songs.append(song)
                #catch exceptions and show popup error
                except Exception as e:
                    popupContent = BoxLayout(orientation='vertical')
                    popupText = Label(text=f"Failed to load library. Please ensure all files are valid audio files.")
                    more_info_btn = Button(text="More Info (for nerds)", size_hint_y=None, height=40)
                    more_info_btn.bind(on_release=lambda x: App.get_running_app().show_error_details(str(e)))
                    popupContent.add_widget(popupText)
                    popupContent.add_widget(more_info_btn)

                    popup = Popup(
                        title="Error",
                        content=popupContent,
                        size_hint=(0.7, 0.4)
                    )

                    popup.open()
        
        self.__isLoaded = True
        return self.all_songs

    def get_all_songs(self):
        if not self.__isLoaded:
            self.load_songs()
        return self.all_songs

    def reload(self):
        self.all_songs = []
        self.__isLoaded = False
        return self.load_songs(force_reload=True)
    

    
    