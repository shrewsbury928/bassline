from kivy.uix.screenmanager import Screen  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        