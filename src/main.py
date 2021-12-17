
__version__ = "0.0.0"

import weakref
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDIconButton
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.list import OneLineListItem, OneLineAvatarIconListItem, TwoLineAvatarIconListItem, IRightBodyTouch
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import FadeTransition, ScreenManager, NoTransition
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.metrics import dp, sp
from kivy.clock import Clock
# local directory
from directories import *
RUNNING_APP = None

#REMOVE/MODIFY IN PRODUCTION
# from kivy.core.window import Window
# Window.size = (dp(428/1.5), dp(926/1.5))
# from decrypt import decryptFile
# decryptFile("")
##############################


class OptionListItem(IRightBodyTouch, MDIconButton):
    adaptive_width = True
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(on_kv_post = self._run_once)

    def _run_once(self, a, b):
        self.bind(on_release=lambda x: RUNNING_APP.open_bottom_sheet())


class OneItemList(OneLineAvatarIconListItem, TouchBehavior):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app = RUNNING_APP

    
    def on_long_touch(self, a, b):
        self.app.open_bottom_sheet()


class TwoItemList(TwoLineAvatarIconListItem, TouchBehavior):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.app = RUNNING_APP
    
    def on_long_touch(self, a, b):
        self.app.open_bottom_sheet()
        

class MenuListItem(OneLineListItem):
    # This is an extension of the ListItem used in the Dropdown menu.
    # It tries to align the labels to the center which was previously more difficult
    # used in the app's menu
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"


class BottomBar(RelativeLayout):
    # Bottom Navigation bar of the app, it includes the recent, local, cloud, and starred pages.
    # This clase extends the pages/tabs functionality.
    # This Class can modify the capitalization and color issues encountered.
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


class TabsWindow(MDScreen):
    #REMOVE/MODIFY IN PRODUCTION
    #for testing purposes
    local_files = [['Project description', 'Today', i%2] if i < 15 else ['Project description', 'Yesterday', 0] for i in range(30)]
    ################################

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.assign_file_to_localTab)
    
    def assign_file_to_localTab(self, a, b):
        #get the list items
        file_list = self.local_files
        
        for name, day, favourite in file_list:
            self.ids.recent_list.add_widget(TwoItemList(text=name, secondary_text=day))
            self.ids.library_list.add_widget(OneItemList(text=name))
            self.ids.cloud_list.add_widget(OneItemList(text=name))
            self.ids.starred_list.add_widget(OneItemList(text=name))


class SignupWindow(MDScreen):
    pass

class LoginWindow(MDScreen):
    pass
        

class MainWidget(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.bind(on_kv_post = self._run_once)
    
    def _run_once(self, d, t):
        self.current = "login"
        Clock.schedule_once(self._open_first_screen)

    def _open_first_screen(self, d):
        self.current = 'tabs'

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
    # keeps track if logged in
    logged_in = BooleanProperty(0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def build(self):
        # Build kivy files
        Builder.load_file(uiSettings_file)
        Builder.load_file(loginWindow_file)
        Builder.load_file(signupWindow_file)
        Builder.load_file(tabs_file)
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

    def open_title_menu(self, inst):
        '''
        called to open menu.
        '''
        menu_names = ("About", "Settings", (lambda x: "Sign in" if not self.logged_in else "Sign out")(None))
        menu_items = [
            {
                "viewclass": "MenuListItem",
                "text": f'{name}',
                "on_release": lambda x= f'{name}': self.close_and_run_menu(x)
            } for name in menu_names
        ]
        menu = MDDropdownMenu(items=menu_items, width_mult=2, max_height=dp(145), radius=[dp(3)])
        menu.caller = inst
        menu.open()

    def close_and_run_menu(self, val):
        '''
        called to close menu and return to the signup page.
        '''
        self.menu.dismiss()
        if val == "Sign in" or val == "Sign out":
            # switch the window to the signup window
            self.root.current = 'signup'
            # manually focus the first text box of the signup window.
            self.root.focus_signup()
    
    def open_profile(self, var):
        self.root.current = 'login'

    def open_bottom_sheet(self):
        obj = MDListBottomSheet()
        obj.add_item('Add to favourite', lambda x: self.add2favourite(), 'star')
        obj.add_item('Delete file', lambda x: self.delete_file(), 'delete')
        obj.add_item('Move file', lambda x: self.move_file(), 'folder-move')
        obj.add_item('Rename file', lambda x: self.rename_file(), 'rename-box')
        obj.add_item('Share file', lambda x: self.share_file(), 'file-send')
        obj.add_item('Download audio', lambda x: self.download_audio(), 'download')
        obj.open()
    
    def add2favourite(self):
        pass
    def delete_file(self):
        pass
    def move_file(self):
        pass
    def rename_file(self):
        pass
    def share_file(self):
        pass
    def download_audio(self):
        pass

if __name__ == "__main__":
    Appobj = TMSApp()
    RUNNING_APP = weakref.ref(Appobj)()
    Appobj.run()
