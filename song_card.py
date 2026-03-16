from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image, CoreImage
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.app import App
import io
from PIL import Image as PILImage


class SongCard(BoxLayout):
    def __init__(self, song=None, album_on_right=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (0.9, None)
        self.height = 120
        self.spacing = 10
        self.padding = [10, 10]
        
        # Store song reference
        self.song = song
        
        # Get title and artist from song if available
        if self.song and hasattr(self.song, 'path'):
            title = self.song.title
            artist = self.song.artist
        else:
            title = 'Unknown Title'
            artist = 'Unknown Artist'

        # Background with rounded corners
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Album art (with image support) - perfect square
        album_art_container = BoxLayout(size_hint=(None, None), size=(100, 100), pos_hint={'center_y': 0.5})
        
        # Try to load album art
        self.album_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Fallback colored rectangle
        with album_art_container.canvas.before:
            Color(0.8, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=album_art_container.pos, size=album_art_container.size)
        album_art_container.bind(pos=self._update_album, size=self._update_album)
        
        # Load cover if available
        if song and hasattr(song, 'cover') and song.cover:
            try:
                if isinstance(song.cover, bytes):
                    # Load image directly from bytes using CoreImage
                    data = io.BytesIO(song.cover)
                    core_image = CoreImage(data, ext='png')
                    self.album_image.texture = core_image.texture
                elif isinstance(song.cover, str):
                    # Load from file path
                    self.album_image.source = song.cover
            except Exception as e:
                print(f"Error loading cover: {e}")
                try:
                    # Try to load default cover
                    self.album_image.source = 'images/Placeholder_Song.png'
                except:
                    pass
        
        album_art_container.add_widget(self.album_image)
        
        # Info section
        info_layout = BoxLayout(orientation='vertical', padding=[5, 10])
        
        # Title label
        title_label = Label(
            text=title,
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.5),
            halign='left',
            valign='bottom',
            color=(1, 1, 1, 1)
        )
        title_label.bind(size=title_label.setter('text_size'))
        info_layout.add_widget(title_label)
        
        # Artist label
        artist_label = Label(
            text=artist,
            font_size='13sp',
            size_hint=(1, 0.5),
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1)
        )
        artist_label.bind(size=artist_label.setter('text_size'))
        info_layout.add_widget(artist_label)
        
        # Play button
        self.play_btn = PlayPauseButton(size_hint=(None, None), size=(30, 30))
        self.play_btn.bind(on_press=self._on_play_pressed)
        
        # Arrange based on album position
        if album_on_right:
            self.add_widget(info_layout)
            self.add_widget(self.play_btn)
            self.add_widget(album_art_container)
        else:
            self.add_widget(album_art_container)
            self.add_widget(info_layout)
            self.add_widget(self.play_btn)
    
    def _on_play_pressed(self, instance):
        """When play button is pressed, load song into audio controller"""
        # Get the audio controller from the app root
        app = App.get_running_app()
        audio_controller = app.root.audio_controller
        
        # Load the single song
        audio_controller.load_song(self.song)
        audio_controller.show_mini()
    
    def _update_bg(self, instance, value):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def _update_album(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size