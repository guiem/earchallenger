#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils.job import Job
from utils.abstract_ctl import AbstractController
from utils.database_manager import EarChallengerDB
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
        screen = self.screen_manager.get_screen(self.screen_name)
        # TODO: done by sqlite now because storage is not present in Kivy 1.7.2
        #from kivy.storage.jsonstore import JsonStore
        #store = JsonStore('settings.json')
        #if store:
        #    screen.num_notes_slider.value = store.get('num_notes')['value']
        dbmgr = EarChallengerDB()
        num_notes = dbmgr.get_setting("num_notes")
        if num_notes != None:
            screen.num_notes_slider.value = num_notes

    def store_num_notes(self, num_notes):
        # TODO: done by sqlite now because storage is not present in Kivy 1.7.2
        #from kivy.storage.jsonstore import JsonStore
        #store = JsonStore('settings.json')
        #store.put('num_notes',value=num_notes)
        dbmgr = EarChallengerDB()
        dbmgr.set_setting("num_notes",num_notes,'int')

    def store_all(self, num_notes):
        self.store_num_notes(num_notes)
        from challenger.challenger_ctl import challenger_ctl
        challenger_ctl.change_num_notes(num_notes)

settings_ctl = SettingsCtl()

