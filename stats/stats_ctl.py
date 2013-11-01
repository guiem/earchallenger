#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils.job import Job
from utils.abstract_ctl import AbstractController
from utils.database_manager import DatabaseManager
import traceback
from kivy.logger import Logger
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import random
import time
from utils.i18n import _
from stats.stats_view import StatsScreen

class StatsCtl(AbstractController):
    screen_name='stats'
     
    def createScreens(self):
        self.screen_manager.add_widget(StatsScreen(name=self.screen_name, controller = self))
         
    def prepareScreen(self):
        screen = self.screen_manager.get_screen(self.screen_name)
        dbmgr = DatabaseManager("earchallenger.db")
        res = dbmgr.query('''SELECT COUNT(*) FROM stats''')
        screen.num_games = res.fetchone()[0]

stats_ctl = StatsCtl()

