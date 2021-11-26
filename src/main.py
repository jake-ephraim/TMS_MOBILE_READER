
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition, ScreenManager, NoTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from directories import *
#REMOVE IN PRODUCTION
#from kivy.core.window import Window
from kivy.metrics import dp, sp
#Window.size = (dp(428/1.5), dp(926/1.5))
from decrypt import decryptFile
decryptFile("")

##############################

class MenuListItem(OneLineListItem):
    # This is an extension of the ListItem used in the Dropdown menu.
    # It tries to align the labels to the center which was previously more difficult
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"


class BottomBar(RelativeLayout):
    # Bottom Navigation bar of the app.
    # This Class tries to modify the capitalization and color issues encountered.
    # This class converts the upper case tab labels to captalized labels.
    # And changes the original blue tab color to our defined color.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_kv_post = self.run_once)
    
    def run_once(self, inst, d):
        '''
        It is called once by the instance of the class when the .kv file is done loading.
        It also tries to access the tab object to change the font  and binds the color to a function, 
        calling it when there is a change in the color value.
        '''
        for i in range(len(self.children[0].children[0].children[0].children)):
            self.children[0].children[0].children[0].children[i].children[0].children[0].font_style = "Subtitle2"
            self.children[0].children[0].children[0].children[i]._text_color_normal = (80/255, 52/255, 24/255, 1) if i == len(self.children[0].children[0].children[0].children)-1 else (80/255, 52/255, 24/255, 0.38)
            self.children[0].children[0].children[0].children[i].bind(_text_color_normal = self.modify_color)

    def modify_color(self, inst, rgba):
        '''
        on every call, this function modifies the color of the tab to the desired color.
        '''
        inst._text_color_normal = (80/255, 52/255, 24/255, rgba[-1])


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
        self.bind(on_kv_post = self.run_once)
    
    def run_once(self, d, t):
        self.current = "signup"
        self.current = "login"
        pass

    def focus_login(self):
        '''
        manually focuses the first input box of the window.
        may not work in future.
        '''
        self.children[0].children[0].children[0].children[-1].children[-1].focus = True


    def focus_signup(self):
        '''
        manually focus the first input box of the window.
        may not work in future.
        '''
        self.children[0].children[0].children[0].children[-1].children[-1].focus = True
        

    
    
    
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
        # Menu Definition
        menu_names = ["About", "Help", "Profile", "Settings", "Sign out"]
        menu_items = [
            {
                "viewclass": "MenuListItem",
                "text": f'{name}',
                "on_release": lambda x= f'{name}': self.menu_return(x)
            } for name in menu_names
        ]
        self.menu = MDDropdownMenu(items=menu_items, width_mult=2, max_height=dp(240), radius=[dp(3)])

        Builder.load_file(uiSettings_file)
        Builder.load_file(loginWindow_file)
        Builder.load_file(signupWindow_file)
        Builder.load_file(recent_file)
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

    def titlebar_menu(self, inst):
        self.menu.caller = inst
        self.menu.open()

    def menu_return(self, val):
        self.menu.dismiss()
        # switch the window to the signup window
        self.root.current = 'signup'
        # manually focus the first text box of the signup window.
        self.root.children[0].children[0].children[0].children[-1].children[-1].focus = True

if __name__ == "__main__":
    TMSApp().run()
