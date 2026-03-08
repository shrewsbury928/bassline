from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.animation import Animation
from Custom_Buttons.play_pause_button import PlayPauseButton
from kivy.app import App
import io
from PIL import Image as PILImage


class SongListItem(BoxLayout):
    """Individual song item in the playlist viewer"""
    def __init__(self, song, playlist, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 60
        self.spacing = 10
        self.padding = [10, 5]
        
        self.song = song
        self.playlist = playlist
        
        # Background
        with self.canvas.before:
            Color(0.55, 0.2, 0.2, 1)  # Darker red
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Album art (small square)
        album_art = BoxLayout(size_hint=(None, 1), width=45, padding=[2, 2])
        with album_art.canvas.before:
            Color(0.65, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=album_art.pos, size=album_art.size)
        album_art.bind(pos=self._update_album, size=self._update_album)
        
        # Song info
        info_layout = BoxLayout(orientation='vertical', padding=[5, 5])
        
        # Get song info
        title = "Unknown Title"
        artist = "Unknown Artist"
        if song:
            try:
                from tinytag import TinyTag
                tags = TinyTag.get(song.path)
                title = tags.title or "Unknown Title"
                artist = tags.artist or "Unknown Artist"
            except:
                pass
        
        title_label = Label(
            text=title,
            font_size='14sp',
            size_hint=(1, 0.6),
            halign='left',
            valign='bottom',
            color=(1, 1, 1, 1)
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        artist_label = Label(
            text=artist,
            font_size='11sp',
            size_hint=(1, 0.4),
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 0.8)
        )
        artist_label.bind(size=artist_label.setter('text_size'))
        
        info_layout.add_widget(title_label)
        info_layout.add_widget(artist_label)
        
        # Play button
        play_btn = PlayPauseButton(size_hint=(None, None), size=(35, 35))
        play_btn.bind(on_press=self._on_play_pressed)
        
        self.add_widget(album_art)
        self.add_widget(info_layout)
        self.add_widget(play_btn)
    
    def _on_play_pressed(self, instance):
        """Play this song"""
        if self.song:
            app = App.get_running_app()
            audio_controller = app.root.audio_controller
            audio_controller.load_song(self.song, self.playlist)
            audio_controller.show_mini()
    
    def _update_bg(self, instance, value):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    def _update_album(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size


class PlaylistViewer(FloatLayout):
    """Floating playlist viewer that slides up from bottom"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (0, 0)  # Start hidden
        
        self.current_playlist = None
        
        # Build UI
        self._build_viewer()
    
    def _build_viewer(self):
        """Build the playlist viewer UI"""
        self.viewer = BoxLayout(orientation='vertical')
        self.viewer.size_hint = (1, 1)
        self.viewer.opacity = 0
        
        # Background color - dark gray
        with self.viewer.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            self.bg = Rectangle(pos=self.viewer.pos, size=self.viewer.size)
        self.viewer.bind(pos=self._update_bg, size=self._update_bg)
        
        # Top bar with back button
        top_bar = BoxLayout(size_hint=(1, 0.08), padding=[10, 5])
        with top_bar.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.top_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_top_rect, pos=self._update_top_rect)
        
        back_btn = Button(
            text='<',
            font_size='30sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=lambda x: self.hide())
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(BoxLayout())
        self.viewer.add_widget(top_bar)
        
        # Main content - scrollable
        scroll_view = ScrollView(size_hint=(1, 0.92))
        content = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=[20, 10, 20, 100],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Album art section
        album_section = BoxLayout(size_hint=(1, None), height=180)
        album_container = BoxLayout(size_hint=(0.5, 1), pos_hint={'center_x': 0.5})
        
        self.album_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        
        with album_container.canvas.before:
            Color(0.65, 0.25, 0.25, 1)
            self.album_art_rect = Rectangle(pos=album_container.pos, size=album_container.size)
        
        with album_container.canvas.after:
            Color(0.15, 0.15, 0.15, 1)
            self.album_border = Line(rectangle=(
                album_container.x, album_container.y,
                album_container.width, album_container.height
            ), width=2)
        
        album_container.bind(pos=self._update_album_art, size=self._update_album_art)
        album_container.add_widget(self.album_image)
        album_section.add_widget(album_container)
        content.add_widget(album_section)
        
        # Title and play button section
        title_section = BoxLayout(size_hint=(1, None), height=60, spacing=10, padding=[10, 0])
        
        self.title_label = Label(
            text='Title',
            font_size='20sp',
            halign='left',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        
        self.main_play_btn = PlayPauseButton(size_hint=(None, None), size=(50, 50))
        self.main_play_btn.bind(on_press=self._play_playlist)
        
        title_section.add_widget(self.title_label)
        title_section.add_widget(self.main_play_btn)
        content.add_widget(title_section)
        
        # Action buttons section
        action_section = BoxLayout(size_hint=(1, None), height=40, spacing=10, padding=[10, 0])
        
        # Edit button
        edit_btn = Button(
            text='Edit',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        edit_btn.bind(on_press=self._show_edit_dialog)
        
        # Add songs button
        add_btn = Button(
            text='Add Songs',
            size_hint=(0.5, 1),
            background_normal='',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        add_btn.bind(on_press=self._show_add_songs_dialog)
        
        action_section.add_widget(edit_btn)
        action_section.add_widget(add_btn)
        content.add_widget(action_section)
        
        # Songs header
        songs_header = Label(
            text='Songs',
            font_size='16sp',
            size_hint=(1, None),
            height=40,
            halign='left',
            valign='middle',
            color=(1, 1, 1, 0.8)
        )
        songs_header.bind(size=songs_header.setter('text_size'))
        content.add_widget(songs_header)
        
        # Songs list container
        self.songs_container = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_y=None
        )
        self.songs_container.bind(minimum_height=self.songs_container.setter('height'))
        content.add_widget(self.songs_container)
        
        scroll_view.add_widget(content)
        self.viewer.add_widget(scroll_view)
        self.add_widget(self.viewer)
    
    def load_playlist(self, playlist):
        """Load a playlist into the viewer"""
        self.current_playlist = playlist
        
        # Update UI with playlist info
        self.title_label.text = playlist.title if playlist else 'Playlist'
        
        # Load cover art if available
        if playlist and hasattr(playlist, 'cover') and playlist.cover:
            try:
                if isinstance(playlist.cover, bytes):
                    image = PILImage.open(io.BytesIO(playlist.cover))
                    temp_path = 'temp_playlist_cover.png'
                    image.save(temp_path)
                    self.album_image.source = temp_path
                elif isinstance(playlist.cover, str):
                    self.album_image.source = playlist.cover
            except Exception as e:
                print(f"Could not load playlist cover: {e}")
                self.album_image.source = ''
        else:
            self.album_image.source = ''
        
        # Load songs
        self._refresh_songs()
    
    def show(self):
        """Show the playlist viewer with animation"""
        print(f"PlaylistViewer.show() called")
        self.size = Window.size
        
        # Animate in
        anim = Animation(opacity=1, duration=0.3, t='out_quad')
        anim.start(self.viewer)
        print(f"Animation started, opacity: {self.viewer.opacity}")
    
    
    def hide(self):
        """Hide the playlist viewer"""
        anim = Animation(opacity=0, duration=0.3, t='out_quad')
        anim.bind(on_complete=lambda *args: setattr(self, 'size', (0, 0)))
        anim.start(self.viewer)
    
    def _refresh_songs(self):
        """Refresh the songs list"""
        self.songs_container.clear_widgets()
        
        if self.current_playlist and hasattr(self.current_playlist, 'songs'):
            if len(self.current_playlist.songs) == 0:
                # Show empty state
                empty_label = Label(
                    text='No songs yet\nTap "Add Songs" to get started',
                    font_size='14sp',
                    size_hint=(1, None),
                    height=80,
                    halign='center',
                    valign='middle',
                    color=(0.7, 0.7, 0.7, 1)
                )
                empty_label.bind(size=empty_label.setter('text_size'))
                self.songs_container.add_widget(empty_label)
            else:
                # Add song items
                for song in self.current_playlist.songs:
                    song_item = SongListItem(song, self.current_playlist)
                    self.songs_container.add_widget(song_item)
    
    def _play_playlist(self, instance):
        """Play the entire playlist"""
        if self.current_playlist and len(self.current_playlist.songs) > 0:
            app = App.get_running_app()
            audio_controller = app.root.audio_controller
            audio_controller.load_playlist(self.current_playlist)
            audio_controller.play()
            audio_controller.show_mini()
    
    def _show_edit_dialog(self, instance):
        """Show dialog to edit playlist name/description"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title input
        content.add_widget(Label(text='Playlist Name:', size_hint_y=0.2))
        title_input = TextInput(
            multiline=False,
            size_hint_y=0.2,
            text=self.current_playlist.title if self.current_playlist else ''
        )
        content.add_widget(title_input)
        
        # Description input
        content.add_widget(Label(text='Description:', size_hint_y=0.2))
        desc_input = TextInput(
            multiline=True,
            size_hint_y=0.4,
            text=self.current_playlist.description if self.current_playlist else ''
        )
        content.add_widget(desc_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        popup = Popup(
            title='Edit Playlist',
            content=content,
            size_hint=(0.85, 0.6)
        )
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=popup.dismiss)
        
        save_btn = Button(
            text='Save',
            background_color=(0.4, 0.5, 0.75, 1),
            background_normal=''
        )
        
        def on_save(instance):
            if self.current_playlist:
                self.current_playlist.title = title_input.text.strip()
                self.current_playlist.description = desc_input.text.strip()
                self.title_label.text = self.current_playlist.title
                
                # Refresh library to show updated name
                app = App.get_running_app()
                library_screen = app.root.screen_manager.get_screen('library')
                library_screen.refresh_library()
            popup.dismiss()
        
        save_btn.bind(on_press=on_save)
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(save_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def _show_add_songs_dialog(self, instance):
        """Show dialog to add songs from file system"""
        # Simple file path input for now
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(
            text='Enter song file path:',
            size_hint_y=0.2
        ))
        
        path_input = TextInput(
            multiline=False,
            size_hint_y=0.3,
            hint_text='/path/to/song.mp3'
        )
        content.add_widget(path_input)
        
        info_label = Label(
            text='Tip: You can add multiple songs by\nentering paths one at a time',
            size_hint_y=0.3,
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        content.add_widget(info_label)
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        popup = Popup(
            title='Add Song',
            content=content,
            size_hint=(0.85, 0.5)
        )
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=popup.dismiss)
        
        add_btn = Button(
            text='Add',
            background_color=(0.4, 0.5, 0.75, 1),
            background_normal=''
        )
        
        def on_add(instance):
            path = path_input.text.strip()
            if path and self.current_playlist:
                try:
                    from song import Song
                    new_song = Song(path)
                    self.current_playlist.add_song(new_song)
                    self._refresh_songs()
                    path_input.text = ''  # Clear for next song
                except Exception as e:
                    error_popup = Popup(
                        title='Error',
                        content=Label(text=f'Could not add song:\n{str(e)}'),
                        size_hint=(0.7, 0.3)
                    )
                    error_popup.open()
        
        add_btn.bind(on_press=on_add)
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(add_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def _update_top_rect(self, instance, value):
        self.top_rect.pos = instance.pos
        self.top_rect.size = instance.size
    
    def _update_album_art(self, instance, value):
        self.album_art_rect.pos = instance.pos
        self.album_art_rect.size = instance.size
        self.album_border.rectangle = (
            instance.x, instance.y,
            instance.width, instance.height
        )