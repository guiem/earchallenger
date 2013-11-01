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
from settings.settings_ctl import settings_ctl
from stats.stats_ctl import stats_ctl

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
        challenger_ctl.play_sequence(self.buttons)

    def btn_next(self):
        challenger_ctl.play_next(self.buttons)
         
    def btn_answer(self,btn_cancel):
        # TODO: do functionality it in controller via self.screen
        state,feedback = challenger_ctl.answer()
        self.btn_answer_label = state
        self.solution = feedback
        if state == _('Submit'):
            btn_cancel.active = True
        elif state == _('Answer'):
            btn_cancel.active = False
         
    def btn_solution(self):
        # TODO: check if return values could be updated in controller through self.screen
        self.solution,self.hints = challenger_ctl.show_solution()
    
    def btn_hints(self):
        self.solution,self.hints = challenger_ctl.show_solution(self.hints)
         
    def btn_cancel(self):
        challenger_ctl.cancel(self.buttons)

    def btn_settings(self):
        settings_ctl.showScreen()

    def btn_statistics(self):
        stats_ctl.showScreen()

from challenger.challenger_ctl import challenger_ctl
