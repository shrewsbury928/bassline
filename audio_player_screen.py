from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.core.window import Window
from Custom_Buttons.play_pause_button import PlayPauseButton

class AudioPlayerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Set background color to light blue
        with main_layout.canvas.before:
            Color(0.65, 0.72, 0.82, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Top bar
        top_bar = BoxLayout(size_hint=(1, 0.08), padding=[10, 5])
        with top_bar.canvas.before:
            Color(0.2, 0.2, 0.2, 0.3)
            self.top_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_top_rect, pos=self._update_top_rect)
        
        back_btn = Button(
            text='⌄',
            font_size='30sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=self.go_back)
        
        top_label = Label(
            text='Audio Controller',
            color=(1, 1, 1, 0.8),
            size_hint=(0.85, 1),
            halign='left',
            valign='middle'
        )
        top_label.bind(size=top_label.setter('text_size'))
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(top_label)
        main_layout.add_widget(top_bar)
        
        # Main content
        content = BoxLayout(orientation='vertical', padding=[40, 60], spacing=30)
        
        content.add_widget(Label(
            text='Playlist/Album Name',
            font_size='18sp',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 0.9)
        ))
        
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
        content.add_widget(album_art_container)
        
        self.progress_slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint=(1, 0.08),
            cursor_size=(15, 15)
        )
        content.add_widget(self.progress_slider)
        
        content.add_widget(Label(
            text='Song Name - Artist Name',
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 0.9)
        ))
        
        controls = BoxLayout(size_hint=(1, 0.1), spacing=20, pos_hint={'center_x': 0.5})
        controls.add_widget(BoxLayout(size_hint=(0.3, 1)))
        
        prev_btn = Button(
            text='⏮',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        play_btn = Button(
            text='▶',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        next_btn = Button(
            text='⏭',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        controls.add_widget(prev_btn)
        controls.add_widget(play_btn)
        controls.add_widget(next_btn)
        controls.add_widget(BoxLayout(size_hint=(0.3, 1)))
        
        content.add_widget(controls)
        content.add_widget(BoxLayout(size_hint=(1, 0.2)))
        
        main_layout.add_widget(content)
        self.add_widget(main_layout)
    
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
    
    def go_back(self, instance):
        self.manager.current = 'home'
