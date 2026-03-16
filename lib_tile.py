from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import CoreImage, Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.app import App
import io
from PIL import Image as PILImage


class LibraryTile(BoxLayout):
    """Square tile for library grid view"""
    def __init__(self, playlist=None, **kwargs):
        print(f"\n=== LibraryTile.__init__ START ===")
        print(f"playlist parameter: {playlist}")
        print(f"playlist type: {type(playlist)}")
        if playlist:
            print(f"playlist.title: {playlist.title}")
        print(f"kwargs: {kwargs}")
        
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (120, 150)
        self.spacing = 0
        self.padding = 0
        
        # Store playlist reference
        self.playlist = playlist
        
        # Get title and description from playlist if available
        description = ""
        if playlist:
            title = playlist.title
            description = playlist.description if hasattr(playlist, 'description') and playlist.description else ""
        
        tile_content = BoxLayout(orientation='vertical', spacing=0, padding=0)

        # Album art section - perfect square (120x120 pixels)
        album_art_section = BoxLayout(size_hint=(1, None), height=120)
        with album_art_section.canvas.before:
            Color(0.65, 0.25, 0.25, 1)  # RED background
            self.album_art_rect = Rectangle(pos=album_art_section.pos, size=album_art_section.size)
        album_art_section.bind(pos=self._update_album_art_rect, size=self._update_album_art_rect)

        # Clickable cover image button inside the square
        cover_path = ""
        if playlist and hasattr(playlist, 'cover') and playlist.cover:
            cover_path = playlist.cover
        
        expand = Button(
            background_normal=cover_path if cover_path else '',
            background_down=cover_path if cover_path else '',
            size_hint=(1, 1)
        )
        expand.bind(on_press=self._on_tile_pressed)
        album_art_section.add_widget(expand)
        tile_content.add_widget(album_art_section)
        
        # Bottom info section with title and description
        bottom_section = BoxLayout(orientation='horizontal', size_hint=(1, None), height=30, padding=[5, 5])
        with bottom_section.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Dark background for info section
            self.bottom_section_rect = Rectangle(pos=bottom_section.pos, size=bottom_section.size)
        bottom_section.bind(pos=self._update_bottom_section_rect, size=self._update_bottom_section_rect)
        
        # Info label
        info_section = Label(
            text=f'{title}',
            font_size='11sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle',
            text_size=(70, None)
        )
        info_section.bind(size=info_section.setter('text_size'))
        bottom_section.add_widget(info_section)
        
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
        
        tile_content.add_widget(bottom_section)
        self.add_widget(tile_content)
    
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
                        data = io.BytesIO(self.playlist.cover)
                        core_image = CoreImage(data, ext='png')
                        self.album_image.texture = core_image.texture
                    elif isinstance(self.playlist.cover, str):
                        self.album_image.source = self.playlist.cover
                except Exception as e:
                    print(f"Could not load library tile cover: {e}")
    
    def _on_tile_pressed(self, instance):
        """When tile body is clicked, open the playlist viewer"""
        print(f"Tile pressed! Playlist: {self.playlist if self.playlist else 'None'}")

        if not self.playlist:
            print("ERROR: No playlist assigned to this tile!")
            return

        print(f"Opening viewer for playlist: {self.playlist.title}")
        
        # Get the playlist viewer from the app root
        app = App.get_running_app()
        print(f"App: {app}")
        print(f"App root: {app.root}")
        print(f"App root type: {type(app.root)}")
        print(f"App root attributes: {dir(app.root)}")
        
        # Check if playlist_viewer exists
        if not hasattr(app.root, 'playlist_viewer'):
            print("ERROR: app.root doesn't have playlist_viewer!")
            print("Make sure you're using the updated main.py file")
            return
        
        playlist_viewer = app.root.playlist_viewer
        print(f"Playlist viewer found: {playlist_viewer}")
        
        # Load the playlist and show the viewer
        playlist_viewer.load_playlist(self.playlist)
        playlist_viewer.show()
    
    def _on_play_pressed(self, instance):
        """When play button is pressed, play the playlist directly"""
        print(f"Play button pressed on tile!")
        
        if self.playlist:
            print(f"Loading playlist: {self.playlist.title}")
            # Get the audio controller from the app root
            app = App.get_running_app()
            audio_controller = app.root.audio_controller
            
            # Load the playlist and play
            if hasattr(self.playlist, 'songs') and len(self.playlist.songs) > 0:
                print(f"Playing {len(self.playlist.songs)} songs")
                audio_controller.load_playlist(self.playlist)
                audio_controller.play()
                audio_controller.show_mini()
            else:
                print("Playlist has no songs")
        
        # Return True to stop propagation to tile click
        return True
    
    def _update_bottom_section_rect(self, instance, value):
        self.bottom_section_rect.pos = instance.pos
        self.bottom_section_rect.size = instance.size
    
    def _update_album_art_rect(self, instance, value):
        self.album_art_rect.pos = instance.pos
        self.album_art_rect.size = instance.size