#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.clock import Clock

class AbstractController:
    def set_screen_manager(self,screen_manager):
        self.screen_manager=screen_manager
    def createScreens(self):
        raise 'Not implemented'
    def prepareScreen(self):
        pass
    def postShowScreen(self,*largs):
        pass
    def showScreen(self):
        self.prepareScreen()
        self.screen_manager.current=self.screen_name
        Clock.schedule_once(self.postShowScreen,1)
    def get_screen(self):
        return self.screen_manager.get_screen(self.screen_name)
