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
from kivy.properties import StringProperty, ObjectProperty
from glob import glob
from os.path import dirname, join, basename
from kivy.logger import Logger

class AudioButton(Button):

    filename = StringProperty(None)

    sound = ObjectProperty(None)

    def on_filename(self, instance, value):
        # the first time that the filename is set, we are loading the sample
        if self.sound is None:
            self.sound = SoundLoader.load(value)

    def on_press(self):
        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        self.sound.play()


class AudioBackground(StackLayout):
    pass


class AudioApp(App):

    def build(self):

        root = AudioBackground(spacing=5)
        root.add_widget(Label(text='Audio example', font_size=32, size_hint_y=None))
        for fn in glob('./resources/instruments/alto_sax/*.wav'): # TODO: find a generic way to address sound directory
            btn = AudioButton(
                text=basename(fn[:-4]).split('_')[1], filename=fn,
                size_hint=(None, None), halign='center',
                size=(128, 128), text_size=(118, None))
            root.add_widget(btn)

        return root

if __name__ == '__main__':
    AudioApp().run()
