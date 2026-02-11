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
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Set background color to dark gray/black
        with main_layout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=Window.size, pos=(0, 0))
        main_layout.add_widget(Label(text="Search Screen - Coming Soon!", color=(1, 1, 1, 1), font_size='24sp'))
        self.add_widget(main_layout)
