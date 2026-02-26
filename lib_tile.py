from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.app import App
import io
from PIL import Image as PILImage


class ClickableTileContainer(ButtonBehavior, BoxLayout):
    """Clickable container for the tile"""
    pass


class LibraryTile(BoxLayout):
    """Square tile for library grid view"""
    def __init__(self, playlist=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (120, 120)
        self.spacing = 0
        self.padding = 0
        
        # Store playlist reference
        self.playlist = playlist
        
        # Get title and description from playlist if available
        title = "Untitled"
        description = ""
        if playlist:
            title = playlist.title if playlist.title else "Untitled"
            description = playlist.description if hasattr(playlist, 'description') and playlist.description else ""
        
        # Main container with rounded corners and red background
        # Make this clickable
        tile_container = ClickableTileContainer(orientation='vertical', padding=0, spacing=0)
        tile_container.bind(on_press=self._on_tile_pressed)
        
        # Background with rounded corners
        with tile_container.canvas.before:
            Color(0.65, 0.25, 0.25, 1)  # Red color
            self.bg = RoundedRectangle(pos=tile_container.pos, size=tile_container.size, radius=[10])
        tile_container.bind(pos=self._update_bg, size=self._update_bg)
        
        # Album art area (takes most of the space)
        album_art_container = BoxLayout(size_hint=(1, 0.5))
        
        # Try to load cover art
        self.album_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Load cover if available
        if playlist and hasattr(playlist, 'cover') and playlist.cover:
            try:
                if isinstance(playlist.cover, bytes):
                    image = PILImage.open(io.BytesIO(playlist.cover))
                    temp_path = f'temp_lib_cover_{id(self)}.png'
                    image.save(temp_path)
                    self.album_image.source = temp_path
                elif isinstance(playlist.cover, str):
                    self.album_image.source = playlist.cover
            except Exception as e:
                print(f"Could not load library tile cover: {e}")
        
        album_art_container.add_widget(self.album_image)
        tile_container.add_widget(album_art_container)
        
        # Info section with title and description
        info_section = BoxLayout(orientation='vertical', size_hint=(1, 0.35), padding=[8, 5, 8, 5])
        
        # Title label
        self.title_label = Label(
            text=title,
            font_size='13sp',
            bold=True,
            size_hint=(1, None),
            height=20,
            halign='left',
            valign='top',
            color=(1, 1, 1, 1),
            text_size=(104, None),  # Fixed width for text wrapping
            shorten=True,
            shorten_from='right'
        )
        
        # Description label (smaller, grayed out)
        self.desc_label = Label(
            text=description,
            font_size='10sp',
            size_hint=(1, None),
            height=30,
            halign='left',
            valign='top',
            color=(0.8, 0.8, 0.8, 1),
            text_size=(104, None),
            markup=True
        )
        
        info_section.add_widget(self.title_label)
        info_section.add_widget(self.desc_label)
        tile_container.add_widget(info_section)
        
        # Bottom section with play button
        bottom_section = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), padding=[5, 0, 5, 5])
        
        # Spacer
        bottom_section.add_widget(BoxLayout(size_hint=(0.7, 1)))
        
        # Play button in bottom right
        self.play_btn = PlayPauseButton(size_hint=(None, None), size=(25, 25))
        self.play_btn.bind(on_press=self._on_play_pressed)
        
        # Container for play button to position it in bottom right
        play_btn_container = BoxLayout(size_hint=(0.3, 1))
        play_btn_anchor = BoxLayout(orientation='vertical')
        play_btn_anchor.add_widget(BoxLayout())  # Spacer top
        play_btn_anchor.add_widget(self.play_btn)
        play_btn_container.add_widget(play_btn_anchor)
        
        bottom_section.add_widget(play_btn_container)
        
        tile_container.add_widget(bottom_section)
        self.add_widget(tile_container)
        self.tile_container = tile_container
    
    def update_display(self):
        """Update the tile display with current playlist info"""
        if self.playlist:
            title = self.playlist.title if self.playlist.title else "Untitled"
            description = self.playlist.description if hasattr(self.playlist, 'description') and self.playlist.description else ""
            
            self.title_label.text = title
            self.desc_label.text = description
            
            # Update cover art if available
            if hasattr(self.playlist, 'cover') and self.playlist.cover:
                try:
                    if isinstance(self.playlist.cover, bytes):
                        image = PILImage.open(io.BytesIO(self.playlist.cover))
                        temp_path = f'temp_lib_cover_{id(self)}.png'
                        image.save(temp_path)
                        self.album_image.source = temp_path
                    elif isinstance(self.playlist.cover, str):
                        self.album_image.source = self.playlist.cover
                except Exception as e:
                    print(f"Could not load library tile cover: {e}")
    
    def _on_tile_pressed(self, instance):
        """When tile body is clicked, open the playlist viewer"""
        if self.playlist:
            # Get the playlist viewer from the app root
            app = App.get_running_app()
            playlist_viewer = app.root.playlist_viewer
            
            # Load the playlist and show the viewer
            playlist_viewer.load_playlist(self.playlist)
            playlist_viewer.show()
    
    def _on_play_pressed(self, instance):
        """When play button is pressed, play the playlist directly"""
        if self.playlist:
            # Get the audio controller from the app root
            app = App.get_running_app()
            audio_controller = app.root.audio_controller
            
            # Load the playlist and play
            if hasattr(self.playlist, 'songs') and len(self.playlist.songs) > 0:
                audio_controller.load_playlist(self.playlist)
                audio_controller.play()
                audio_controller.show_mini()
        
        return True  # Stop propagation to prevent tile click
    
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size