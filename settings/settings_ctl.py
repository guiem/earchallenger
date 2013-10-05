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
        screen =self.screen_manager.get_screen(self.screen_name)
    
settings_ctl = SettingsCtl()

