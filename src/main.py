
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition, ScreenManager, NoTransition
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from directories import *
#REMOVE IN PRODUCTION
from kivy.core.window import Window
from kivy.metrics import dp, sp
Window.size = (dp(428/1), dp(926/1))
##############################

class RecentWindow(MDScreen):
    pass


class SignupWindow(MDScreen):
    pass


class LoginWindow(MDScreen):
    pass
        

class MainWidget(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        Clock.schedule_once(self.run_once, 1)
    
    def run_once(self, dt):
        self.current = "login"
    
    
    
class TMSApp(MDApp):
    # Dynamic fonts
    font_size_1 = ObjectProperty(dp(30))
    font_size_2 = ObjectProperty(dp(24))
    font_size_3 = ObjectProperty(dp(20))
    # Static fonts
    font_size_30 = ObjectProperty(dp(30))
    font_size_24 = ObjectProperty(dp(24))
    font_size_20 = ObjectProperty(dp(20))
    font_size_16 = ObjectProperty(dp(16))
    font_size_14 = ObjectProperty(dp(14))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def build(self):
        Builder.load_file(uiSettings_file)
        Builder.load_file(loginWindow_file)
        Builder.load_file(signupWindow_file)
        #Builder.load_file(template_file)
        #Builder.load_file(recent_file)
        Builder.load_file(components_file)
        rootWindow = Builder.load_file(mainKivy_file)
        return rootWindow
    
    def update_fonts(self, width, height):
        ## responsive font settings 
        min_font_size = 18
        max_screen_size = 1000
        # responsive size 30dp 24dp 20dp
        self.font_size_1 = sp(min_font_size + (min( min(height, width), max_screen_size) * 28.037383/max_screen_size))
        self.font_size_2 = sp(min_font_size + (min( min(height, width), max_screen_size) * 14.018691/max_screen_size))
        self.font_size_3 = sp(min_font_size + (min( min(height, width), max_screen_size) * 4.672897/max_screen_size))


if __name__ == "__main__":
    TMSApp().run()