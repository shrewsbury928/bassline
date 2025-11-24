from kivy.app import App
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.uix.widget import Widget
from kivy.core.window import Window
import library
import library.song as song_module

class DemoApp(App):
    def build(self):
        root = Widget()
        btn = PlayPauseButton(size_hint=(None, None), size=(40, 40))
        btn.pos = ( (Window.width - btn.width) / 2, (Window.height - btn.height) / 2)
        root.add_widget(btn)

        #ong = song_module.Song(r'C:\Users\shrey\OneDrive - st-bernards.slough.sch.uk\A level comp-sci\CO3 - NEA\Bassline\bassline\library\test_song.mp3',None,"lofi" )
        #song.play()
        return root
    
    def pause_resume(self):
        self.song.un_pause()

if __name__ == '__main__':
    DemoApp().run()
