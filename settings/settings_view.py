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
from challenger.challenger_ctl import challenger_ctl

Builder.load_file('settings/settings.kv')

class SettingsScreen(Screen):

    def button_back(self):
        challenger_ctl.showScreen()

    def button_save(self):
        pass

from settings.settings_ctl import settings_ctl
