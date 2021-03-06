'''
Audio example
=============

All the sounds are from the http://www.compositiontoday.com/sound_bank/alto_saxophone/alto_saxophone.asp
"Composition:Today"

'''

import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, ListProperty,BooleanProperty
from glob import glob
from os.path import dirname, join, basename
from kivy.logger import Logger
import gettext
import os
from main_ctl import main_ctl
from utils.i18n import _

# Set up message catalog access
dir = os.path.dirname(__file__)
languagePath = os.path.join(dir, 'language')
gettext.bindtextdomain('multilingual', languagePath)

class MyScreenManager(ScreenManager):
    all_widgets_disabled = BooleanProperty(False)

    def dispatch(self,*args,**kwargs):
        if not self.all_widgets_disabled:
            return super(MyScreenManager,self).dispatch(*args,**kwargs)
        else:
            return None

class EarChallengerApp(App):
    
    # TODO: deprecated?
    def get_answer(self):
        return self.answer
         
    def on_pause(self):
        return True

    def build(self):
        self.set_language('en_US')
        #self.set_language('es')
        self.root = MyScreenManager()
        main_ctl.setScreenManager(self.root)
        main_ctl.gotoChallenger()
        return self.root
        
    def set_language(self,selectedLanguage):
        self.t = gettext.translation('multilingual', languagePath, languages=[selectedLanguage], fallback=True)
        _ = self.t.ugettext #The 'u' in 'ugettext' is for Unicode - use this to keep Unicode from breaking the app
        #self.root.greeting = _('Hello!')
    
    def get_text(self, *args):
        return self.t.ugettext(*args)
    
if __name__ == '__main__':
    EarChallengerApp().run()
