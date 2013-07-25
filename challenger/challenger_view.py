#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.logger import Logger
from glob import glob
from os.path import dirname, join, basename

Builder.load_file('challenger/challenger.kv')

class AudioButton(Button):
    filename = StringProperty(None)
    sound = ObjectProperty(None)

    def on_filename(self, instance, value):
        # the first time that the filename is set, we are loading the sample
        if self.sound is None:
            self.sound = SoundLoader.load(value)

    def on_press(self):
        challenger_ctl.press_audio_btn(self)

class ChallengerScreen(Screen):
    grid = ObjectProperty()
    buttons = ListProperty([])
    answer = ListProperty([])
    num_notes = 5 # TODO: make dropdown list
    solution = StringProperty('')
    btn_answer_label = StringProperty('Answer')
     
    def prepare(self):
        Logger.debug('ChallengerScreen: into prepare')
        for fn in glob('resources/instruments/alto_sax/*.wav'): # TODO: find a generic way to address sound directory
            Logger.debug('ChallengerScreen: entro')
            btn = AudioButton(text=basename(fn[:-4]).split('_')[1], filename=fn,size_hint=(1.0, None), halign='center', text_size=(None, None)) 
            self.grid.add_widget(btn)
            self.buttons.append(btn)

    def btn_play(self):
        challenger_ctl.play_sequence(self.buttons,self.num_notes)
    
    def btn_next(self):
        challenger_ctl.play_next(self.buttons,self.num_notes)
         
    def btn_answer(self):
        state,feedback = challenger_ctl.answer()
        self.btn_answer_label = state
        self.solution = feedback
         
    def btn_solution(self):
        self.solution = challenger_ctl.show_solution(self.solution)

from challenger.challenger_ctl import challenger_ctl
