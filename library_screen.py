from kivy.uix.screenmanager import Screen  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from library_tile import LibraryTile
from playlist import Playlist


class LibraryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.username = "USER"
        self.user_playlists = []  # Store user's playlists
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Set background color to dark gray/black
        with main_layout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Top header with profile circle, title, and create button
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), padding=[20, 15], spacing=15)
        
        # Profile circle (blue)
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
        
        # Create playlist button
        create_btn = Button(
            text='+',
            font_size='32sp',
            size_hint=(None, None),
            width=60,
            height=60,
            background_normal='',
            background_color=(0.4, 0.5, 0.75, 1),
            color=(1, 1, 1, 1)
        )
        create_btn.bind(on_press=self.create_playlist_dialog)
        
        header.add_widget(profile_circle)
        header.add_widget(self.title_label)
        header.add_widget(create_btn)
        main_layout.add_widget(header)
        
        # Scrollable content area for grid
        scroll_view = ScrollView(size_hint=(1, 0.88))
        
        # Grid layout for tiles (2 columns)
        self.grid_layout = GridLayout(
            cols=2,
            spacing=15,
            padding=[20, 10, 20, 100],  # Extra bottom padding for mini player
            size_hint_y=None,
            row_default_height=120,
            row_force_default=True
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        
        # Grid starts empty - user can add playlists with the + button
        
        scroll_view.add_widget(self.grid_layout)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)
    
    def set_username(self, username):
        """Update username in the library title"""
        self.username = username
        self.title_label.text = f"{username}'s\nLibrary"
    
    def create_playlist_dialog(self, instance):
        """Show dialog to create a new playlist"""
        # Create dialog content
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title input
        content.add_widget(Label(text='Playlist Name:', size_hint_y=0.3))
        title_input = TextInput(
            multiline=False,
            size_hint_y=0.3,
            hint_text='Enter playlist name'
        )
        content.add_widget(title_input)
        
        # Description input
        content.add_widget(Label(text='Description (optional):', size_hint_y=0.3))
        desc_input = TextInput(
            multiline=True,
            size_hint_y=0.5,
            hint_text='Enter description'
        )
        content.add_widget(desc_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.4, spacing=10)
        
        # Create popup first so we can reference it in callbacks
        popup = Popup(
            title='Create New Playlist',
            content=content,
            size_hint=(0.85, 0.6)
        )
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=popup.dismiss)
        
        create_btn = Button(
            text='Create',
            background_color=(0.4, 0.5, 0.75, 1),
            background_normal=''
        )
        
        def on_create(instance):
            title = title_input.text.strip()
            if not title:
                # Show error if no title
                error_popup = Popup(
                    title='Error',
                    content=Label(text='Please enter a playlist name'),
                    size_hint=(0.7, 0.3)
                )
                error_popup.open()
                return
            
            # Create new playlist
            new_playlist = Playlist(title, desc_input.text.strip())
            self.user_playlists.append(new_playlist)
            
            # Refresh the grid
            self.refresh_library()
            popup.dismiss()
        
        create_btn.bind(on_press=on_create)
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(create_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def refresh_library(self):
        """Refresh the library grid with current playlists"""
        self.grid_layout.clear_widgets()
        for playlist in self.user_playlists:
            tile = LibraryTile(playlist=playlist)
            self.grid_layout.add_widget(tile)
    
    def load_playlists(self, playlists):
        """Load user's playlists into the grid"""
        self.user_playlists = playlists
        self.refresh_library()
    
    def _update_circle(self, instance, value):
        self.circle.pos = instance.pos
        self.circle.size = instance.size