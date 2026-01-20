from kivy.uix.screenmanager import Screen  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from Custom_Buttons.play_pause_button import PlayPauseButton
from song_card import SongCard

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.username = "USER"
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Set background color
        with main_layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Top header
        header = BoxLayout(size_hint=(1, 0.06), padding=[15, 10])
        with header.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header, pos=self._update_header)
        
        header.add_widget(Label(
            text='Homepage',
            color=(0.6, 0.6, 0.6, 1),
            halign='left',
            valign='middle'
        ))
        main_layout.add_widget(header)
        
        # Welcome section
        welcome_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), padding=[20, 15], spacing=15)
        
        # Profile circle (blue)
        profile_circle = BoxLayout(size_hint=(None, None), width=60, height=60)
        with profile_circle.canvas:
            Color(0.4, 0.5, 0.75, 1)
            self.circle = Rectangle(pos=profile_circle.pos, size=profile_circle.size)
        profile_circle.bind(pos=self._update_circle, size=self._update_circle)
        
        self.welcome_label = Label(
            text=f'Welcome,\n{self.username}',
            font_size='20sp',
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        self.welcome_label.bind(size=self.welcome_label.setter('text_size'))
        
        welcome_box.add_widget(profile_circle)
        welcome_box.add_widget(self.welcome_label)
        main_layout.add_widget(welcome_box)
        
        # Scrollable content area for song cards
        scroll_view = ScrollView(size_hint=(1, 0.67))
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[20, 10],
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Add song cards (alternating album position)
        content_layout.add_widget(SongCard("Title", "Description", album_on_right=False))
        content_layout.add_widget(SongCard("Title", "Description", album_on_right=True))
        content_layout.add_widget(SongCard("Title", "Description", album_on_right=False))
        content_layout.add_widget(SongCard("Title", "Description", album_on_right=True))
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        #util = BoxLayout(size_hint=(1, 0.01))

        self.add_widget(main_layout)
    
    def set_username(self, username):
        self.username = username
        self.welcome_label.text = f'Welcome,\n[{username}]'
    
    def _update_header(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
    
    def _update_circle(self, instance, value):
        self.circle.pos = instance.pos
        self.circle.size = instance.size
    
    def _update_player(self, instance, value):
        self.player_rect.pos = instance.pos
        self.player_rect.size = instance.size
