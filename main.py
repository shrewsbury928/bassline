from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.core.window import Window

# Import your backend functions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from backend import login as backend


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Set background color
        with layout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Welcome title
        title = Label(
            text='WELCOME TO\nBASSLINE',
            font_size='28sp',
            size_hint=(1, 0.3),
            bold=True,
            halign='center'
        )
        layout.add_widget(title)
        
        # Username field
        layout.add_widget(Label(text='Username:', size_hint=(1, 0.1), halign='left'))
        self.username_input = TextInput(
            multiline=False,
            size_hint=(1, 0.15),
            background_color=(0.85, 0.85, 0.85, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10]
        )
        layout.add_widget(self.username_input)
        
        # Email field
        layout.add_widget(Label(text='Email:', size_hint=(1, 0.1), halign='left'))
        self.email_input = TextInput(
            multiline=False,
            size_hint=(1, 0.15),
            background_color=(0.85, 0.85, 0.85, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10]
        )
        layout.add_widget(self.email_input)
        
        # Password field
        layout.add_widget(Label(text='Password:', size_hint=(1, 0.1), halign='left'))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint=(1, 0.15),
            background_color=(0.85, 0.85, 0.85, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10]
        )
        layout.add_widget(self.password_input)
        
        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.15), spacing=20)
        
        login_btn = Button(
            text='Login',
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal=''
        )
        login_btn.bind(on_press=self.login_pressed)
        
        register_btn = Button(
            text='Register',
            background_color=(0.3, 0.5, 0.8, 1),
            background_normal=''
        )
        register_btn.bind(on_press=self.register_pressed)
        
        button_layout.add_widget(login_btn)
        button_layout.add_widget(register_btn)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def login_pressed(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text
        
        if not username or not email or not password:
            self.show_popup('Error', 'Please fill in all fields')
            return
        
        result = backend.login(username, email, password)
        
        if result is True:
            # Store username and clear fields
            self.manager.get_screen('home').set_username(username)
            self.username_input.text = ''
            self.email_input.text = ''
            self.password_input.text = ''
            # Switch to home screen
            self.manager.current = 'home'
        else:
            self.show_popup('Login Failed', str(result))
    
    def register_pressed(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text
        
        if not username or not email or not password:
            self.show_popup('Error', 'Please fill in all fields')
            return
        
        result = backend.register(username, email, password)
        
        if result is True:
            # Store username and clear fields
            self.manager.get_screen('home').set_username(username)
            self.username_input.text = ''
            self.email_input.text = ''
            self.password_input.text = ''
            # Switch to home screen
            self.manager.current = 'home'
        elif result is False:
            self.show_popup('Registration Failed', 'Username or email already exists')
        elif isinstance(result, list):
            error_msg = '\n'.join(result)
            self.show_popup('Registration Failed', error_msg)
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.7, 0.4)
        )
        popup.open()


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
        
        # Play button
        play_btn = Button(
            text='▶',
            font_size='30sp',
            size_hint=(None, None),
            width=50,
            height=50,
            pos_hint={'center_y': 0.5},
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        
        # Arrange based on album position
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
            text=f'Welcome,\n[USER]',
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
        
        # Bottom player bar
        player_bar = BoxLayout(orientation='vertical', size_hint=(1, 0.15), padding=[15, 10], spacing=5)
        with player_bar.canvas.before:
            Color(0.5, 0.55, 0.65, 1)
            self.player_rect = RoundedRectangle(pos=player_bar.pos, size=player_bar.size, radius=[10])
        player_bar.bind(size=self._update_player, pos=self._update_player)
        
        # Song info and controls
        player_controls = BoxLayout(orientation='horizontal', size_hint=(1, 0.6), spacing=10)
        
        play_btn = Button(
            text='▶',
            font_size='28sp',
            size_hint=(None, 1),
            width=50,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        
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
        
        # Navigation buttons
        nav_buttons = BoxLayout(size_hint=(1, 0.4), spacing=15, padding=[0, 5])
        
        for i in range(3):
            nav_btn = Button(
                text='',
                size_hint=(0.33, 1),
                background_color=(0.4, 0.5, 0.75, 1),
                background_normal=''
            )
            with nav_btn.canvas.before:
                Color(0.4, 0.5, 0.75, 1)
            nav_buttons.add_widget(nav_btn)
        
        player_bar.add_widget(nav_buttons)
        main_layout.add_widget(player_bar)
        
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


class AudioPlayerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Set background color to light blue
        with main_layout.canvas.before:
            Color(0.65, 0.72, 0.82, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Top bar
        top_bar = BoxLayout(size_hint=(1, 0.08), padding=[10, 5])
        with top_bar.canvas.before:
            Color(0.2, 0.2, 0.2, 0.3)
            self.top_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_top_rect, pos=self._update_top_rect)
        
        back_btn = Button(
            text='⌄',
            font_size='30sp',
            size_hint=(0.15, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        back_btn.bind(on_press=self.go_back)
        
        top_label = Label(
            text='Audio Controller',
            color=(1, 1, 1, 0.8),
            size_hint=(0.85, 1),
            halign='left',
            valign='middle'
        )
        top_label.bind(size=top_label.setter('text_size'))
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(top_label)
        main_layout.add_widget(top_bar)
        
        # Main content
        content = BoxLayout(orientation='vertical', padding=[40, 60], spacing=30)
        
        content.add_widget(Label(
            text='Playlist/Album Name',
            font_size='18sp',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 0.9)
        ))
        
        # Album art
        album_art_container = BoxLayout(size_hint=(1, 0.4))
        album_art = BoxLayout(size_hint=(0.7, 1), pos_hint={'center_x': 0.5})
        
        with album_art.canvas.before:
            Color(0.65, 0.25, 0.25, 1)
            self.album_rect = Rectangle(pos=album_art.pos, size=album_art.size)
        
        with album_art.canvas.after:
            Color(0.15, 0.15, 0.15, 1)
            self.album_border = Line(rectangle=(
                album_art.x, album_art.y,
                album_art.width, album_art.height
            ), width=3)
        
        album_art.bind(pos=self._update_album_art, size=self._update_album_art)
        album_art_container.add_widget(album_art)
        content.add_widget(album_art_container)
        
        self.progress_slider = Slider(
            min=0,
            max=100,
            value=50,
            size_hint=(1, 0.08),
            cursor_size=(15, 15)
        )
        content.add_widget(self.progress_slider)
        
        content.add_widget(Label(
            text='Song Name - Artist Name',
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 0.9)
        ))
        
        controls = BoxLayout(size_hint=(1, 0.1), spacing=20, pos_hint={'center_x': 0.5})
        controls.add_widget(BoxLayout(size_hint=(0.3, 1)))
        
        prev_btn = Button(
            text='⏮',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        play_btn = Button(
            text='▶',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        next_btn = Button(
            text='⏭',
            font_size='35sp',
            size_hint=(0.13, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 0.9)
        )
        
        controls.add_widget(prev_btn)
        controls.add_widget(play_btn)
        controls.add_widget(next_btn)
        controls.add_widget(BoxLayout(size_hint=(0.3, 1)))
        
        content.add_widget(controls)
        content.add_widget(BoxLayout(size_hint=(1, 0.2)))
        
        main_layout.add_widget(content)
        self.add_widget(main_layout)
    
    def _update_top_rect(self, instance, value):
        self.top_rect.pos = instance.pos
        self.top_rect.size = instance.size
    
    def _update_album_art(self, instance, value):
        self.album_rect.pos = instance.pos
        self.album_rect.size = instance.size
        self.album_border.rectangle = (
            instance.x, instance.y,
            instance.width, instance.height
        )
    
    def go_back(self, instance):
        self.manager.current = 'home'


class BasslineApp(App):
    def build(self):
        # Set fixed mobile resolution
        Window.size = (360, 640)  # Width, Height in pixels
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AudioPlayerScreen(name='audio_player'))
        
        return sm


if __name__ == '__main__':
    BasslineApp().run()