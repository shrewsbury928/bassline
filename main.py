from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color

import sys
import os

# Import screens
from home_screen import HomeScreen
from login_screen import LoginScreen
from library_screen import LibraryScreen
from search_screen import SearchScreen

# Import audio controller
from audio_controller import AudioController

# Import song/playlist classes
from song import Song
from playlist import Playlist


class MainContainer(FloatLayout):
    #contruct the app
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Screen manager for pages
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(LibraryScreen(name='library'))
        self.screen_manager.add_widget(SearchScreen(name='search'))
        
        # Bind to screen changes to show/hide nav bar
        self.screen_manager.bind(current=self._on_screen_change)
        
        self.add_widget(self.screen_manager)
        
        # Navigation bar at bottom (initially hidden)
        self.nav_bar = BoxLayout(size_hint=(0.9, None), height=60, spacing=15, pos_hint={'center_x': 0.5, 'y': 0.02})
        self.nav_bar.opacity = 0  # Hide on login screen
        
        lib_btn = Button(
            text='Library',
            size_hint=(0.33, 1),
            background_normal='',
            background_color=(0.4, 0.5, 0.75, 1)
        )
        lib_btn.bind(on_press=lambda x: setattr(self.screen_manager, 'current', 'library'))
        
        home_btn = Button(
            text='Home',
            size_hint=(0.33, 1),
            background_normal='',
            background_color=(0.4, 0.5, 0.75, 1)
        )
        home_btn.bind(on_press=lambda x: setattr(self.screen_manager, 'current', 'home'))
        
        search_btn = Button(
            text='Search',
            size_hint=(0.33, 1),
            background_normal='',
            background_color=(0.4, 0.5, 0.75, 1)
        )
        search_btn.bind(on_press=lambda x: setattr(self.screen_manager, 'current', 'search'))

        self.nav_bar.add_widget(lib_btn)
        self.nav_bar.add_widget(home_btn)
        self.nav_bar.add_widget(search_btn)
        
        # Add nav bar BEFORE audio controller
        self.add_widget(self.nav_bar)
        
        # Floating audio controller (on top of everything) - ADD THIS LAST!
        self.audio_controller = AudioController()
        self.add_widget(self.audio_controller)
    
    def _on_screen_change(self, instance, value):
        #show nav bar on all screens except login
        if value == 'login':
            self.nav_bar.opacity = 0
        else:
            self.nav_bar.opacity = 1


class BasslineApp(App):
    def build(self):
        # Set fixed mobile resolution
        Window.size = (360, 640)
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        
        return MainContainer()


if __name__ == '__main__':
    from kivy.config import Config
    Config.set('graphics', 'resizable', False)
    
    BasslineApp().run()
    