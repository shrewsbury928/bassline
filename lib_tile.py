from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.app import App
import io
from PIL import Image as PILImage


class LibraryTile(BoxLayout):
    #square tile with playlist information
    def __init__(self, playlist=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (120, 120)
        self.spacing = 0
        self.padding = 0
        
        # Store playlist reference
        self.playlist = playlist
        
        # Get title from playlist if available
        title = "Title"
        if playlist:
            title = playlist.title
        
        # Main container with rounded corners and red background
        tile_container = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # Background with rounded corners
        with tile_container.canvas.before:
            Color(0.65, 0.25, 0.25, 1)  # Red color
            self.bg = RoundedRectangle(pos=tile_container.pos, size=tile_container.size, radius=[10])
        tile_container.bind(pos=self._update_bg, size=self._update_bg)
        
        # Album art area (takes most of the space)
        album_art_container = BoxLayout(size_hint=(1, 0.7))
        
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
        
        # Bottom section with title and play button
        bottom_section = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), padding=[5, 0, 5, 5])
        
        # Title label
        title_label = Label(
            text=title,
            font_size='12sp',
            size_hint=(0.7, 1),
            halign='left',
            valign='bottom',
            color=(1, 1, 1, 1)
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Play button in bottom right
        self.play_btn = PlayPauseButton(size_hint=(None, None), size=(25, 25))
        self.play_btn.bind(on_press=self._on_play_pressed)
        
        # Container for play button to position it in bottom right
        play_btn_container = BoxLayout(size_hint=(0.3, 1))
        play_btn_container.add_widget(BoxLayout())  # Spacer
        play_btn_anchor = BoxLayout(orientation='vertical')
        play_btn_anchor.add_widget(BoxLayout())  # Spacer top
        play_btn_anchor.add_widget(self.play_btn)
        play_btn_container.add_widget(play_btn_anchor)
        
        bottom_section.add_widget(title_label)
        bottom_section.add_widget(play_btn_container)
        
        tile_container.add_widget(bottom_section)
        self.add_widget(tile_container)
        self.tile_container = tile_container
    
    def _on_play_pressed(self, instance):
        #load playlist into audio controller
        if self.playlist:
            # Get the audio controller from the app root
            app = App.get_running_app()
            audio_controller = app.root.audio_controller
            
            # Load the playlist and show mini player
            audio_controller.load_playlist(self.playlist)
            audio_controller.play()
            audio_controller.show_mini()
    
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size