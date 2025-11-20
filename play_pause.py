from kivy.app import App
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.uix.widget import Widget
from kivy.core.window import Window
import kivy_layouts, songs
import backend.song as song_module

class DemoApp(App):
    def build(self):
        root = Widget()
        btn = PlayPauseButton(size_hint=(None, None), size=(40, 40))
        btn.pos = ( (Window.width - btn.width) / 2, (Window.height - btn.height) / 2)
        root.add_widget(btn)

        song = song_module.Song(songs.test_song,None,"lofi" )
        song.play()
        return root
    
    def pause_resume(self):
        self.song.un_pause()

if __name__ == '__main__':
    DemoApp().run()
