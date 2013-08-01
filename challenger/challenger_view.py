#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.logger import Logger
from glob import glob
from os.path import dirname, join, basename
from utils.i18n import _

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
    played_times = NumericProperty(0)
    hints = NumericProperty(0)

    def prepare(self):
        Logger.debug('ChallengerScreen: into prepare')
        for fn in glob('resources/instruments/alto_sax/*.wav'): # TODO: find a generic way to address sound directory
            Logger.debug('ChallengerScreen: entro')
            btn = AudioButton(text=basename(fn[:-4]).split('_')[1], filename=fn,size_hint=(1.0,1.0), halign='center', text_size=(None, None)) 
            self.grid.add_widget(btn)
            self.buttons.append(btn)

    def btn_play(self):
        challenger_ctl.play_sequence(self.buttons,self.num_notes)
        self.played_times += 1

    def btn_next(self):
        challenger_ctl.play_next(self.buttons,self.num_notes)
        self.played_times = 1
        self.hints = 0
        self.solution = ''
         
    def btn_answer(self,btn_cancel):
        state,feedback = challenger_ctl.answer()
        self.btn_answer_label = state
        self.solution = feedback
        if state == _('Submit'):
            btn_cancel.active = True
        elif state == _('Answer'):
            btn_cancel.active = False
         
    def btn_solution(self):
        self.solution,self.hints = challenger_ctl.show_solution(self.num_notes-1)
    
    def btn_hints(self):
        if self.hints != self.num_notes:
            self.solution,self.hints = challenger_ctl.show_solution(self.hints)
         
    def btn_cancel(self):
        challenger_ctl.cancel(self.buttons)

from challenger.challenger_ctl import challenger_ctl
