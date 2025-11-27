import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from Custom_Buttons.play_pause_button import PlayPauseButton
from song import Song


class SongCard(BoxLayout):
    def __init__(self, title="Title", description="Description", album_on_right=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (0.9, None)
        self.height = 120
        self.spacing = 10
        self.padding = [10, 10]
        
        # Background with rounded corners
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Album art (red square)
        album_art = BoxLayout(size_hint=(None, 1), width=80)
        with album_art.canvas:
            Color(0.6, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=album_art.pos, size=album_art.size)
        album_art.bind(pos=self._update_album, size=self._update_album)
        
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
        
        play_btn = PlayPauseButton(size_hint=(None, None), size=(30, 30))
        
        # Arrange based on album cover position
        if album_on_right:
            self.add_widget(info_layout)
            self.add_widget(play_btn)
            self.add_widget(album_art)
        else:
            self.add_widget(album_art)
            self.add_widget(info_layout)
            self.add_widget(play_btn)
        
        self.album_art_widget = album_art
    
    def _update_bg(self, instance, value):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def _update_album(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size

    def get_song(self):
        pass
