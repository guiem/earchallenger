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
from stats.stats_view import StatsScreen

class StatsCtl(AbstractController):
    screen_name='stats'
     
    def createScreens(self):
        self.screen_manager.add_widget(StatsScreen(name=self.screen_name, controller = self))
         
    def prepareScreen(self):
        screen = self.screen_manager.get_screen(self.screen_name)
        dbmgr = EarChallengerDB("earchallenger.db")
        screen.num_games = dbmgr.get_num_games()

stats_ctl = StatsCtl()

