'''
Audio example
=============

All the sounds are from the http://www.compositiontoday.com/sound_bank/alto_saxophone/alto_saxophone.asp
"Composition:Today"

'''

import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from glob import glob
from os.path import dirname, join, basename
from kivy.logger import Logger
import random
import time
import gettext
import os

# Set up message catalog access
dir = os.path.dirname(__file__)
languagePath = os.path.join(dir, 'language')
gettext.bindtextdomain('multilingual', languagePath)

class AudioButton(Button):

    filename = StringProperty(None)

    sound = ObjectProperty(None)

    def on_filename(self, instance, value):
        # the first time that the filename is set, we are loading the sample
        if self.sound is None:
            self.sound = SoundLoader.load(value)

    def on_press(self):
        app_state = App.get_running_app().state
        if app_state == 'answering':
            self.background_color = [1,1,0,1]
            self.text = self.text + '+'
        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        self.sound.play()

class PlayButton(Button):
    pass     

class NextButton(Button):
    pass     

class SolutionButton(Button):
    pass     

class AnswerButton(Button):
    pass

class AudioBackground(StackLayout):
    pass 

def _(*args):
    return App.get_running_app().get_text(*args)

class AudioApp(App):

    buttons = ListProperty([])
    sequence = ListProperty([])
    answer = ListProperty([])
    state = StringProperty('normal')
    num_notes = 5 # TODO: make dropdown list 

    def get_answer(self):
        return self.answer

    def _create_sequence(self):
        seq = []
        for i in range(self.num_notes):
            seq.append(self.buttons[random.randint(0,len(self.buttons)-1)])
        return seq

    def _print_solution(self):
        solution = []
        for note in self.sequence:
            solution.append(note.text)
        return (',').join(solution)
        
    def answer(self):
        Logger.debug('Guiem: entro amb estat ' + str(self.state))
        if self.state == 'normal':
            self.state = 'answering'
        elif self.state == 'answering':
            self.state = 'normal'

    def play_sequence(self):
        if not self.sequence:
            self.sequence = self._create_sequence()
        for btn in self.sequence:
            btn.sound.play()
            time.sleep(1) # TODO: check if there is a proper way to pause between sounds. Moreover: make speed adjustable by bar
            btn.sound.stop()
             
    def next_sequence(self):
        self.sequence = []
        self.play_sequence()
    
    def solution_sequence(self,solution_label):
        solution_label.text = self._print_solution()
         
    def on_pause(self):
        return True

    def build(self):
        self.set_language('en_US') 
        root = AudioBackground(spacing=5)
        root.add_widget(Label(text=_('Tap your answer'), font_size=32, size_hint_y=None))
        for fn in glob('./resources/instruments/alto_sax/*.wav'): # TODO: find a generic way to address sound directory
            btn = AudioButton(
                text=basename(fn[:-4]).split('_')[1], filename=fn,
                size_hint=(None, None), halign='center',
                size=(128, 128), text_size=(118, None))
            root.add_widget(btn)
            self.buttons.append(btn)

        return root

    def set_language(self,selectedLanguage):
        self.t = gettext.translation('multilingual', languagePath, languages=[selectedLanguage], fallback=True)
        _ = self.t.ugettext #The 'u' in 'ugettext' is for Unicode - use this to keep Unicode from breaking the app
        #self.root.greeting = _('Hello!')
    
    def get_text(self, *args):
        return self.t.ugettext(*args)
    

if __name__ == '__main__':
    AudioApp().run()
