from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.image import Image, CoreImage
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from Custom_Buttons.play_pause_button import PlayPauseButton
import pygame.mixer as mixer
import io
from PIL import Image as PILImage

class AudioController(FloatLayout):
    """Floating audio controller that can be minimized or expanded"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_expanded = False
        self.size_hint = (None, None)
        self.size = (0, 0)  # Start hidden
        
        # Queue system
        self.queue = []  # List of songs to play
        self.current_index = 0  # Current position in queue
        
        # Current playlist and song tracking
        self.current_playlist = None  # Reference to source playlist (for metadata)
        self.current_song = None
        
        # Track song start time for accurate seeking
        self.song_start_time = 0  # When the current song started playing
        self.seek_offset = 0  # Offset from manual seeking
        
        # Initialize pygame mixer with music
        try:
            mixer.init()
        except:
            pass
        
        # Schedule position update
        self.update_event = None
        
        # Build UI
        self._build_mini_player()
        self._build_full_player()
        
    def _build_mini_player(self):
        """Build the mini player UI - horizontal bar at bottom"""
        # Container for mini player with proper positioning
        # Custom container that only captures touches within mini player bounds
        class MiniPlayerContainer(FloatLayout):
            def __init__(self, audio_controller, **kwargs):
                super().__init__(**kwargs)
                self.audio_controller = audio_controller
            
            def on_touch_down(self, touch):
                # Only handle touches if they hit the mini player widget itself
                if not self.audio_controller.mini_player.disabled:
                    if self.audio_controller.mini_player.collide_point(*touch.pos):
                        return super().on_touch_down(touch)
                # Let touches pass through to widgets below
                return False
            
            def on_touch_move(self, touch):
                if not self.audio_controller.mini_player.disabled:
                    if self.audio_controller.mini_player.collide_point(*touch.pos):
                        return super().on_touch_move(touch)
                return False
            
            def on_touch_up(self, touch):
                if not self.audio_controller.mini_player.disabled:
                    if self.audio_controller.mini_player.collide_point(*touch.pos):
                        return super().on_touch_up(touch)
                return False
        
        self.mini_container = MiniPlayerContainer(self, size_hint=(1, 1))
        
        self.mini_player = BoxLayout(orientation='horizontal', size_hint=(0.9, None), height=70, padding=[15, 10], spacing=10)
        self.mini_player.pos_hint = {'center_x': 0.5, 'y': 0.12}
        self.mini_player.opacity = 0
        self.mini_player.disabled = True  # Disable touch events when hidden
        
        with self.mini_player.canvas.before:
            Color(0.5, 0.55, 0.65, 1)
            self.mini_bg = RoundedRectangle(pos=self.mini_player.pos, size=self.mini_player.size, radius=[15])
        self.mini_player.bind(pos=self._update_mini_bg, size=self._update_mini_bg)
        
        # Play button
        self.mini_play_btn = PlayPauseButton(size_hint=(None, None), size=(40, 40))
        self.mini_play_btn.bind(on_press=self.toggle_play_pause)
        
        # Song info
        self.mini_song_label = Label(
            text='No song playing',
            font_size='14sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        self.mini_song_label.bind(size=self.mini_song_label.setter('text_size'))
        
        # Skip buttons
        mini_skip_back = Button(
            text='|<',
            font_size='20sp',
            size_hint=(None, 1),
            width=40,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        mini_skip_back.bind(on_press=lambda x: (print("Mini skip back pressed"), self.previous_song()))
        
        mini_skip_forward = Button(
            text='>|',
            font_size='20sp',
            size_hint=(None, 1),
            width=40,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        mini_skip_forward.bind(on_press=lambda x: (print("Mini skip forward pressed"), self.next_song()))
        
        self.mini_player.add_widget(self.mini_play_btn)
        
        # Make song label clickable to expand
        self.mini_song_label_btn = Button(
            background_color=(0, 0, 0, 0),
            background_normal=''
        )
        self.mini_song_label_btn.bind(on_press=lambda x: self.expand())
        label_container = BoxLayout()
        label_container.add_widget(self.mini_song_label_btn)
        label_container.add_widget(self.mini_song_label)
        
        self.mini_player.add_widget(label_container)
        self.mini_player.add_widget(mini_skip_back)
        self.mini_player.add_widget(mini_skip_forward)
        
        self.mini_container.add_widget(self.mini_player)
        
        self.add_widget(self.mini_container)
        
    def _build_full_player(self):
        """Build the full player UI - full screen overlay"""
        self.full_player = BoxLayout(orientation='vertical')
        self.full_player.size_hint = (1, 1)
        self.full_player.opacity = 0
        self.full_player.disabled = True  # Disable touch events when hidden
        
        # Set background color to match design (light blue)
        with self.full_player.canvas.before:
            Color(0.65, 0.72, 0.82, 1)
            self.full_bg = Rectangle(pos=self.full_player.pos, size=self.full_player.size)
        self.full_player.bind(pos=self._update_full_bg, size=self._update_full_bg)
        
        # Top bar with minimize button
        top_bar = BoxLayout(size_hint=(1, 0.08), padding=[10, 5])
        minimize_btn = Button(
            text='V',
            font_size='30sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        minimize_btn.bind(on_press=lambda x: self.show_mini())
        top_bar.add_widget(minimize_btn)
        top_bar.add_widget(BoxLayout())
        self.full_player.add_widget(top_bar)
        
        # Main content
        content = BoxLayout(orientation='vertical', padding=[40, 40], spacing=30)
        
        # Playlist/Album name
        self.playlist_label = Label(
            text='No Playlist',
            font_size='18sp',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 0.9)
        )
        content.add_widget(self.playlist_label)
        
        # Album art with image support
        album_art_container = BoxLayout(size_hint=(1, 0.45))
        self.album_art_layout = BoxLayout(size_hint=(0.75, 1), pos_hint={'center_x': 0.5})
        
        # Image widget for cover art
        self.album_image = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Fallback colored rectangle
        with self.album_art_layout.canvas.before:
            Color(0.65, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=self.album_art_layout.pos, size=self.album_art_layout.size)
        
        with self.album_art_layout.canvas.after:
            Color(0.15, 0.15, 0.15, 1)
            self.album_border = Line(rectangle=(
                self.album_art_layout.x, self.album_art_layout.y,
                self.album_art_layout.width, self.album_art_layout.height
            ), width=3)
        
        self.album_art_layout.bind(pos=self._update_album_art, size=self._update_album_art)
        self.album_art_layout.add_widget(self.album_image)
        album_art_container.add_widget(self.album_art_layout)
        content.add_widget(album_art_container)
        
        # Progress slider
        self.progress_slider = Slider(
            min=0,
            max=100,
            value=0,
            size_hint=(1, 0.08),
            cursor_size=(15, 15)
        )
        self.progress_slider.bind(on_touch_up=self._on_slider_seek)
        content.add_widget(self.progress_slider)
        
        # Song info
        self.song_label = Label(
            text='No song playing',
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 0.9)
        )
        content.add_widget(self.song_label)
        
        # Control buttons
        controls = BoxLayout(size_hint=(1, 0.12), spacing=20, pos_hint={'center_x': 0.5})
        controls.add_widget(BoxLayout(size_hint=(0.25, 1)))
        
        prev_btn = Button(
            text='|<',
            font_size='35sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        prev_btn.bind(on_press=lambda x: self.previous_song())
        
        self.full_play_btn = PlayPauseButton(size_hint=(None, None), size=(60, 60))
        self.full_play_btn.bind(on_press=self.toggle_play_pause)
        
        next_btn = Button(
            text='>|',
            font_size='35sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        next_btn.bind(on_press=lambda x: self.next_song())
        
        controls.add_widget(prev_btn)
        controls.add_widget(self.full_play_btn)
        controls.add_widget(next_btn)
        controls.add_widget(BoxLayout(size_hint=(0.25, 1)))
        
        content.add_widget(controls)
        content.add_widget(BoxLayout(size_hint=(1, 0.17)))
        
        self.full_player.add_widget(content)
        self.add_widget(self.full_player)
    
    def load_playlist(self, playlist):
        """Load a playlist into the audio controller - adds all songs to queue"""
        print(f"Loading playlist: {playlist.title if playlist else 'None'}")
        self.current_playlist = playlist
        
        if playlist and hasattr(playlist, 'songs') and len(playlist.songs) > 0:
            # Clear current queue and load playlist songs
            self.queue = playlist.songs.copy()  # Copy so we don't modify original
            self.current_index = 0
            self.current_song = self.queue[0]
            print(f"Loaded {len(self.queue)} songs to queue, starting with: {self.current_song}")
            self.update_ui()
        else:
            print("Playlist is empty or has no songs")
            self.queue = []
    
    def load_song(self, song, playlist=None):
        """Load a single song - if part of playlist, loads entire playlist to queue"""
        print(f"Loading single song: {song}")
        
        if playlist and hasattr(playlist, 'songs'):
            # Load entire playlist to queue
            self.current_playlist = playlist
            self.queue = playlist.songs.copy()
            try:
                self.current_index = self.queue.index(song)
                self.current_song = song
                print(f"Loaded playlist '{playlist.title}' to queue ({len(self.queue)} songs), starting at index {self.current_index}")
            except ValueError:
                # Song not in playlist, start at beginning
                self.current_index = 0
                self.current_song = self.queue[0] if self.queue else None
        else:
            # Single song - create queue with just this song
            self.queue = [song]
            self.current_index = 0
            self.current_song = song
            self.current_playlist = None
            print(f"Created queue with single song")
        
        self.update_ui()
        self.play()
    
    def add_to_queue(self, song):
        """Add a song to the end of the queue"""
        self.queue.append(song)
        print(f"Added song to queue. Queue now has {len(self.queue)} songs")
        
        # If nothing is playing, start playing this song
        if not self.current_song:
            self.current_index = 0
            self.current_song = self.queue[0]
            self.update_ui()
            self.play()
    
    def play_next(self, song):
        """Add a song to play next in the queue (after current song)"""
        insert_index = self.current_index + 1
        self.queue.insert(insert_index, song)
        print(f"Added song to play next at index {insert_index}. Queue now has {len(self.queue)} songs")
    
    def get_queue(self):
        """Get the current queue of songs"""
        return self.queue
    
    def clear_queue(self):
        """Clear the queue, keeping only the current song"""
        if self.current_song:
            self.queue = [self.current_song]
            self.current_index = 0
            print("Queue cleared, only current song remaining")
        else:
            self.queue = []
            print("Queue cleared completely")
    
    def update_ui(self):
        """Update UI elements with current song info from tags"""
        if self.current_song:
            try:
                # Get metadata from TinyTag
                from tinytag import TinyTag
                tags = TinyTag.get(self.current_song.path)
                
                title = tags.title or "Unknown Title"
                artist = tags.artist or "Unknown Artist"
                
                # Update labels
                song_text = f"{title} - {artist}"
                self.song_label.text = song_text
                self.mini_song_label.text = song_text
                
                # Update album art from cover bytes
                if hasattr(self.current_song, 'cover') and self.current_song.cover:
                    try:
                        if isinstance(self.current_song.cover, bytes):
                            # Save temporarily
                            data = io.BytesIO(self.current_song.cover)
                            core_image = CoreImage(data, ext='png')
                            self.album_image.texture = core_image.texture
                        elif isinstance(self.current_song.cover, str):
                            self.album_image.source = self.current_song.cover
                    except Exception as e:
                        print(f"Could not load album art: {e}")
                        self.album_image.source = ''
                else:
                    self.album_image.source = ''
                
                # Update playlist name
                if self.current_playlist:
                    self.playlist_label.text = self.current_playlist.title
                
                # Update slider max value
                if tags.duration:
                    self.progress_slider.max = tags.duration
            except Exception as e:
                print(f"Error updating UI: {e}")
                self.song_label.text = 'Song loaded'
                self.mini_song_label.text = 'Song loaded'
        else:
            self.song_label.text = 'No song playing'
            self.mini_song_label.text = 'No song playing'
            self.playlist_label.text = 'No Playlist'
            self.album_image.source = ''
    
    def play(self):
        """Play the current song using mixer.music"""
        if self.current_song and hasattr(self.current_song, 'path'):
            try:
                mixer.music.load(self.current_song.path)
                mixer.music.play()
                self.current_song.paused = False
                
                # Reset seek tracking
                import time
                self.song_start_time = time.time()
                self.seek_offset = 0
                
                self.mini_play_btn.set_playing(True, animate=False)
                self.full_play_btn.set_playing(True, animate=False)
                
                # Start updating progress
                if self.update_event:
                    self.update_event.cancel()
                self.update_event = Clock.schedule_interval(self._update_progress, 0.1)
            except Exception as e:
                print(f"Error playing song: {e}")
    
    def pause(self):
        """Pause the current song"""
        if self.current_song:
            mixer.music.pause()
            self.current_song.paused = True
            self.mini_play_btn.set_playing(False)
            self.full_play_btn.set_playing(False)
            
            # Update seek offset to preserve current position
            import time
            elapsed = (time.time() - self.song_start_time) + self.seek_offset
            self.seek_offset = elapsed
            
            if self.update_event:
                self.update_event.cancel()
    
    def toggle_play_pause(self, instance):
        """Toggle between play and pause"""
        if self.current_song:
            if self.current_song.paused or not mixer.music.get_busy():
                mixer.music.unpause()
                self.current_song.paused = False
                self.mini_play_btn.set_playing(True)
                self.full_play_btn.set_playing(True)
                
                # Reset start time when resuming
                import time
                self.song_start_time = time.time()
                
                if self.update_event:
                    self.update_event.cancel()
                self.update_event = Clock.schedule_interval(self._update_progress, 0.1)
            else:
                self.pause()
    
    def next_song(self):
        """Skip to next song in queue"""
        print(f"next_song called. Queue length: {len(self.queue)}")
        
        if len(self.queue) > 0:
            self.current_index = (self.current_index + 1) % len(self.queue)
            self.current_song = self.queue[self.current_index]
            print(f"Skipping to song {self.current_index + 1}/{len(self.queue)}: {self.current_song}")
            mixer.music.stop()
            self.update_ui()
            self.play()
        else:
            print("Queue is empty")
    
    def previous_song(self):
        """Go to previous song in queue"""
        print(f"previous_song called. Queue length: {len(self.queue)}")
        
        if len(self.queue) > 0:
            self.current_index = (self.current_index - 1) % len(self.queue)
            self.current_song = self.queue[self.current_index]
            print(f"Going back to song {self.current_index + 1}/{len(self.queue)}: {self.current_song}")
            mixer.music.stop()
            self.update_ui()
            self.play()
        else:
            print("Queue is empty")
    
    def _update_progress(self, dt):
        """Update progress slider based on song position"""
        if mixer.music.get_busy():
            # Calculate elapsed time more accurately
            import time
            elapsed = (time.time() - self.song_start_time) + self.seek_offset
            self.progress_slider.value = min(elapsed, self.progress_slider.max)
        else:
            # Song finished
            if len(self.queue) > 1:
                # Auto-advance to next song in queue
                self.next_song()
            else:
                # Queue finished
                if self.update_event:
                    self.update_event.cancel()
                self.mini_play_btn.set_playing(False, animate=False)
                self.full_play_btn.set_playing(False, animate=False)
    
    def _on_slider_seek(self, instance, touch):
        """Handle seeking when slider is moved"""
        if self.progress_slider.collide_point(*touch.pos):
            # Only seek when user releases the slider (on_touch_up)
            if touch.grab_current == self.progress_slider:
                seek_pos = self.progress_slider.value
                print(f"Seeking to {seek_pos} seconds")
                
                if self.current_song and hasattr(self.current_song, 'path'):
                    try:
                        was_playing = mixer.music.get_busy()
                        
                        # Stop current playback
                        mixer.music.stop()
                        
                        # Reload the song
                        mixer.music.load(self.current_song.path)
                        
                        # For MP3 files, we need to simulate seeking by:
                        # 1. Playing from start
                        # 2. Immediately seeking using set_pos (works for some formats)
                        # 3. Tracking offset for progress display
                        
                        if was_playing or not self.current_song.paused:
                            try:
                                # Try native seeking first (works for OGG, limited for MP3)
                                mixer.music.play(start=seek_pos)
                                
                                # Update our time tracking
                                import time
                                self.song_start_time = time.time()
                                self.seek_offset = seek_pos
                                
                                self.current_song.paused = False
                                print(f"Successfully seeked to {seek_pos}s")
                            except Exception as e:
                                # Fallback: play from beginning if seeking fails
                                print(f"Seeking not fully supported for this format: {e}")
                                mixer.music.play()
                                import time
                                self.song_start_time = time.time()
                                self.seek_offset = 0
                        else:
                            # Song was paused, load at position but don't play
                            mixer.music.play(start=seek_pos)
                            mixer.music.pause()
                            import time
                            self.song_start_time = time.time()
                            self.seek_offset = seek_pos
                            
                    except Exception as e:
                        print(f"Error seeking: {e}")
    
    def show_mini(self):
        """Show the mini player with smooth animation"""
        self.is_expanded = False
        self.size = Window.size
        
        # Enable/disable touch events
        self.mini_player.disabled = False
        self.full_player.disabled = True
        
        # Animate the transition
        anim_full = Animation(opacity=0, duration=0.3, t='out_quad')
        anim_mini = Animation(opacity=1, duration=0.3, t='out_quad')
        
        anim_full.start(self.full_player)
        anim_mini.start(self.mini_container)
        anim_mini.start(self.mini_player)
    
    def expand(self):
        """Expand to full player with smooth animation"""
        self.is_expanded = True
        self.size = Window.size
        
        # Enable/disable touch events
        self.mini_player.disabled = True
        self.full_player.disabled = False
        
        # Animate the transition
        anim_mini = Animation(opacity=0, duration=0.3, t='out_quad')
        anim_full = Animation(opacity=1, duration=0.3, t='out_quad')
        
        anim_mini.start(self.mini_container)
        anim_mini.start(self.mini_player)
        anim_full.start(self.full_player)
    
    def hide(self):
        """Completely hide the player"""
        self.size = (0, 0)
        self.mini_container.opacity = 0
        self.mini_player.opacity = 0
        self.full_player.opacity = 0
        
        # Disable touch events for both
        self.mini_player.disabled = True
        self.full_player.disabled = True
    
    def on_touch_down(self, touch):
        """Override to allow touches to pass through when full player is hidden"""
        # If full player is disabled (hidden), don't consume the touch
        if self.full_player.disabled:
            # Only handle touch if it's for the mini player
            if self.mini_player.collide_point(*touch.pos) and not self.mini_player.disabled:
                return super().on_touch_down(touch)
            else:
                # Let touch pass through to widgets below
                return False
        else:
            # Full player is active, handle normally
            return super().on_touch_down(touch)
    
    def _update_mini_bg(self, instance, value):
        self.mini_bg.pos = instance.pos
        self.mini_bg.size = instance.size
    
    def _update_full_bg(self, instance, value):
        self.full_bg.pos = instance.pos
        self.full_bg.size = instance.size
    
    def _update_album_art(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size
        self.album_border.rectangle = (
            instance.x, instance.y,
            instance.width, instance.height
        )