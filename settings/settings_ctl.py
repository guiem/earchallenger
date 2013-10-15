#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils.job import Job
from utils.abstract_ctl import AbstractController
import traceback
from kivy.logger import Logger
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import random
import time
from utils.i18n import _
from settings.settings_view import SettingsScreen


class SettingsCtl(AbstractController):
    screen_name='settings'
     
    def createScreens(self):
        self.screen_manager.add_widget(SettingsScreen(name=self.screen_name, controller = self))
         
    def prepareScreen(self):
        from kivy.storage.jsonstore import JsonStore
        screen = self.screen_manager.get_screen(self.screen_name)
        store = JsonStore('settings.json')
        if store:
            screen.num_notes_slider.value = store.get('num_notes')['value']

    def store_num_notes(self, num_notes):
        from kivy.storage.jsonstore import JsonStore
        store = JsonStore('settings.json')
        store.put('num_notes',value=num_notes)

    def store_all(self, num_notes):
        self.store_num_notes(num_notes)
        from challenger.challenger_ctl import challenger_ctl
        challenger_ctl.change_num_notes(num_notes)

settings_ctl = SettingsCtl()

