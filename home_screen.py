from kivy.uix.screenmanager import Screen  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import random as r
from song_card import SongCard
from recommendation_engine import RecommendationEngine
from songs_manager import library


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
        scroll_view = ScrollView(size_hint=(1, 0.82))
        self.content_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[20, 10, 20, 100],  # Extra bottom padding for mini player
            size_hint_y=None
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        # Load recommended songs
        self.load_recommendations()
        
        scroll_view.add_widget(self.content_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def load_recommendations(self):
        """Load recommended songs and create song cards"""
        try:
            engine = RecommendationEngine()
            songs = engine.get_random_recommendations(count=r.randint(4, 7))

            if len(songs) == 0:
                # No songs found - show message
                self.content_layout.add_widget(Label(
                    text='No songs found!\nAdd MP3 files to the "songs" folder',
                    font_size='16sp',
                    color=(0.7, 0.7, 0.7, 1),
                    size_hint_y=None,
                    height=100
                ))
            else:
                # Create song cards alternating left/right
                for i, song in enumerate(songs):
                    album_on_right = (i % 2 == 1)
                    card = SongCard(song=song, album_on_right=album_on_right)
                    self.content_layout.add_widget(card)
        
        except Exception as e:
            print(f"Error loading recommendations: {e}")
            # Show error message
            self.content_layout.add_widget(Label(
                text=f'Error loading songs:\n{str(e)}',
                font_size='14sp',
                color=(1, 0.3, 0.3, 1),
                size_hint_y=None,
                height=100
            ))
    
    def refresh_recommendations(self):
        """Reload recommendations (can be called when user wants new suggestions)"""
        self.content_layout.clear_widgets()
        self.load_recommendations()
    
    def set_username(self, username):
        self.username = username
        self.welcome_label.text = f'Welcome,\n[{username}]'
    
    def _update_header(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
    
    def _update_circle(self, instance, value):
        self.circle.pos = instance.pos
        self.circle.size = instance.size