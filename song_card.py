from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.app import App
import io
from PIL import Image as PILImage


class SongCard(BoxLayout):
    def __init__(self, song=None, playlist=None, album_on_right=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (0.9, None)
        self.height = 120
        self.spacing = 10
        self.padding = [10, 10]
        
        # Store song and playlist references
        self.song = song
        self.playlist = playlist
        
        # Get title and description from song if available
        title = "Title"
        description = "Description"
        
        if song:
            try:
                from tinytag import TinyTag
                tags = TinyTag.get(song.path)
                title = tags.title or "Unknown Title"
                description = tags.artist or "Unknown Artist"
            except:
                pass
        
        # Background with rounded corners
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Album art (with image support)
        album_art_container = BoxLayout(size_hint=(None, 1), width=80)
        
        # Try to load album art
        self.album_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Fallback colored rectangle
        with album_art_container.canvas.before:
            Color(0.6, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=album_art_container.pos, size=album_art_container.size)
        album_art_container.bind(pos=self._update_album, size=self._update_album)
        
        # Load cover if available
        if song and hasattr(song, 'cover') and song.cover:
            try:
                if isinstance(song.cover, bytes):
                    image = PILImage.open(io.BytesIO(song.cover))
                    temp_path = f'temp_cover_{id(self)}.png'
                    image.save(temp_path)
                    self.album_image.source = temp_path
                elif isinstance(song.cover, str):
                    self.album_image.source = song.cover
            except Exception as e:
                print(f"Could not load card cover: {e}")
        
        album_art_container.add_widget(self.album_image)
        
        # Info section
        info_layout = BoxLayout(orientation='vertical', padding=[5, 10])
        info_layout.add_widget(Label(
            text=title,
            font_size='16sp',
            bold=True,
            size_hint=(1, 0.5),
            halign='left',
            valign='bottom',
            color=(1, 1, 1, 1)
        ))
        desc_label = Label(
            text=description,
            font_size='13sp',
            size_hint=(1, 0.5),
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1)
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        info_layout.add_widget(desc_label)
        
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
        if self.song:
            # Get the audio controller from the app root
            app = App.get_running_app()
            audio_controller = app.root.audio_controller
            
            # Load the song and show mini player
            audio_controller.load_song(self.song, self.playlist)
            audio_controller.show_mini()
    
    def _update_bg(self, instance, value):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def _update_album(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size