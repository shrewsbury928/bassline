from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# Import your backend functions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

#screens
from home_screen import HomeScreen
from audio_player_screen import AudioPlayerScreen
from login_screen import LoginScreen


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