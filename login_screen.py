
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
from Custom_Buttons.play_pause_button import PlayPauseButton

# Import your backend functions
from backend import login

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
            password=False,
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
        
        result = login.login(username, email, password)
        
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
        
        result = login.register(username, email, password)
        
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
