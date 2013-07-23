#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from challenger.challenger_ctl import challenger_ctl
from utils.abstract_ctl import AbstractController
from kivy.logger import Logger

class MainCtl(AbstractController):
    controllers=[challenger_ctl]
    
    def setScreenManager(self,manager):
        self.screen_manager=manager
        for c in self.controllers:
            c.set_screen_manager(manager)
            c.createScreens()
    
    def gotoChallenger(self):
        challenger_ctl.showScreen()

main_ctl=MainCtl()

