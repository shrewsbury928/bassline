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

        # Bottom player bar
        player_bar = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=[15, 15], spacing=5)
        with player_bar.canvas.before:
            Color(0.5, 0.55, 0.65, 1)
            self.player_rect = RoundedRectangle(pos=player_bar.pos, size=player_bar.size, radius=[10])
        player_bar.bind(size=self._update_player, pos=self._update_player)
        
        # Song info and controls
        player_controls = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), spacing=10)
        
        play_btn = PlayPauseButton(size_hint=(None, None), size=(40, 40))
        
        player_controls.add_widget(play_btn)
        player_controls.add_widget(Label(
            text='Song Name - Artist Name',
            font_size='14sp',
            color=(1, 1, 1, 1),
            halign='left'
        ))
        
        skip_back = Button(
            text='⏮',
            font_size='24sp',
            size_hint=(None, 1),
            width=50,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        
        skip_forward = Button(
            text='⏭',
            font_size='24sp',
            size_hint=(None, 1),
            width=50,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        
        player_controls.add_widget(skip_back)
        player_controls.add_widget(skip_forward)
        player_bar.add_widget(player_controls)

        main_layout.add_widget(player_bar)
        #util.add_widget(player_bar)

        # Navigation buttons
        nav_buttons = BoxLayout(size_hint=(1, 0.1), spacing=15, padding=[0, 5])
        
        lib_btn = Button(
            text='Library',
            size_hint=(0.33, 1),
            background_color=(0.4, 0.5, 0.75, 1),
            background_normal=''
        )
        with lib_btn.canvas.before:
            Color(0.4, 0.5, 0.75, 1)
        nav_buttons.add_widget(lib_btn)
    
        home_btn = Button(
            text='Home',
            size_hint=(0.33, 1),
            background_color=(0.4, 0.5, 0.75, 1),
            background_normal=''
        )
        with home_btn.canvas.before:
            Color(0.4, 0.5, 0.75, 1)
        nav_buttons.add_widget(home_btn)

        search_btn = Button(
            text='Search',
            size_hint=(0.33, 1),
            background_color=(0.4, 0.5, 0.75, 1),
            background_normal=''
        )
        with search_btn.canvas.before:
            Color(0.4, 0.5, 0.75, 1)
        nav_buttons.add_widget(search_btn)

        
        main_layout.add_widget(nav_buttons)
        
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
