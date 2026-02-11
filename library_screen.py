from kivy.uix.screenmanager import Screen  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from lib_tile import LibraryTile
from recommendation_engine import RecommendationEngine


class LibraryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.username = "USER"
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Set background color to dark gray/black
        with main_layout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Top header with profile circle and title
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), padding=[20, 15], spacing=15)
        
        # Profile circle
        profile_circle = BoxLayout(size_hint=(None, None), width=60, height=60)
        with profile_circle.canvas:
            Color(0.4, 0.5, 0.75, 1)
            self.circle = Rectangle(pos=profile_circle.pos, size=profile_circle.size)
        profile_circle.bind(pos=self._update_circle, size=self._update_circle)
        
        # Title label
        self.title_label = Label(
            text=f"{self.username}'s\nLibrary",
            font_size='20sp',
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        
        header.add_widget(profile_circle)
        header.add_widget(self.title_label)
        main_layout.add_widget(header)
        
        # Scrollable content area for grid
        scroll_view = ScrollView(size_hint=(1, 0.88))
        
        # set 2 column grid
        self.grid_layout = GridLayout(
            cols=2,
            spacing=15,
            padding=[20, 10, 20, 100],  #padding for scroll space
            size_hint_y=None,
            row_default_height=120,
            row_force_default=True
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        
        # SAMPLE TILES
        for i in range(7):
            tile = LibraryTile(playlist=None)
            self.grid_layout.add_widget(tile)
        
        scroll_view.add_widget(self.grid_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def set_username(self, username):
        self.username = username
        self.title_label.text = f"{username}'s\nLibrary"
    
    def load_playlists(self, playlists):
        self.grid_layout.clear_widgets()
        for playlist in playlists:
            tile = LibraryTile(playlist=playlist)
            self.grid_layout.add_widget(tile)

    def create_recommended_playlist(self):
        # Placeholder for recommended playlist creation logic
        engine = RecommendationEngine()
        rand_songs = engine.get_random_recommendations()
        playlist = engine.create_playlist_from_songs(rand_songs, title="SAMPLE", description="TEST")

    def create_playlist(self):
        # Placeholder for playlist creation logic
        pass
    
    def _update_circle(self, instance, value):
        self.circle.pos = instance.pos
        self.circle.size = instance.size