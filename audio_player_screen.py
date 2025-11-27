from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
#from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.core.window import Window
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.uix.behaviors.button import ButtonBehaviour

class AudioPlayerScreen(BoxLayout, ButtonBehaviour):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.is_mini = False
        
        layout = BoxLayout()
        
        # Set background color to light blue
        with layout.canvas.before:
            Color(0.65, 0.72, 0.82, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Back Button
        top_bar = BoxLayout(orientation='horizontal', size_hint = (1, 0.2))
        with top_bar.canvas.before:
            Color(0,0,0,0)
            self.top_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_top_rect, pos=self._update_top_rect)
        
        back_btn = Button(
            text='⌄',
            font_size='30sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=self.switch_layout)
        top_bar.add_widget(back_btn)
        
        # Main content       
        playlist_info = Label(
            text='Playlist/Album Name',
            font_size='18sp',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 0.9)
        )
        
        # Album art
        album_art_container = BoxLayout(size_hint=(1, 0.4))
        album_art = BoxLayout(size_hint=(0.7, 1), pos_hint={'center_x': 0.5})
        
        with album_art.canvas.before:
            Color(0.65, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=album_art.pos, size=album_art.size)
        
        with album_art.canvas.after:
            Color(0.15, 0.15, 0.15, 1)
            self.album_border = Line(rectangle=(
                album_art.x, album_art.y,
                album_art.width, album_art.height
            ), width=3)
        
        album_art.bind(pos=self._update_album_art, size=self._update_album_art)
        album_art_container.add_widget(album_art)
        
        self.progress_slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint=(1, 0.08),
            cursor_size=(15, 15)
        )
        
        song_info = Label(
            text='Song Name - Artist Name',
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 0.9)
        )
        
        controls = BoxLayout(size_hint=(1, 0.1), spacing=20, pos_hint={'center_x': 0.5})
        controls.add_widget(BoxLayout(size_hint=(0.3, 1)))
        
        prev_btn = Button(
            text='|<',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        play_btn = PlayPauseButton(size_hint=(None, None), size=(40, 40))

        next_btn = Button(
            text='>|',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        controls.add_widget(prev_btn)
        controls.add_widget(play_btn)
        controls.add_widget(next_btn)
        controls.add_widget(BoxLayout(size_hint=(0.3, 1)))

        if self.is_mini == False:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(top_bar)
            layout.add_widget(playlist_info)
            layout.add_widget(album_art_container)
            layout.add_widget(self.progress_slider)
            layout.add_widget(song_info)
            layout.add_widget(controls)
            
        else:
            layout = BoxLayout(size_hint=(0.3, 1), orientation='horizontal')
            layout.add_widget(album_art_container)
            layout.add_widget(song_info)
            layout.add_widget(controls)
            layout.bind(on_press=self.switch_layout)
    
    def _update_top_rect(self, instance, value):
        self.top_rect.pos = instance.pos
        self.top_rect.size = instance.size
    
    def _update_album_art(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size
        self.album_border.rectangle = (
            instance.x, instance.y,
            instance.width, instance.height
        )
    
    def switch_layout(self):
        self.is_mini = not self.is_mini

        
