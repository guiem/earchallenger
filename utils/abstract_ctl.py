#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.clock import Clock

from kivy.event import EventDispatcher

from kivy.properties import ObjectProperty,BooleanProperty

class AbstractController(EventDispatcher):
    item_selection=BooleanProperty(False)
    item_selection_callback=ObjectProperty(None,allownone=True)
    def set_screen_manager(self,screen_manager):
        self.screen_manager=screen_manager
    def createScreens(self):
        raise 'Not implemented'
    def prepareScreen(self):
        pass
    def postShowScreen(self,*largs):
        pass
    def showScreen(self,**kwargs):
        self.item_selection=False
        self.item_selection_callback=None
        if 'item_selection' in kwargs:
            self.item_selection=kwargs['item_selection']
        if 'item_selection_callback' in kwargs:
            self.item_selection_callback=kwargs['item_selection_callback']
        self.prepareScreen()
        self.screen_manager.current=self.screen_name
        Clock.schedule_once(self.postShowScreen,1)
    def get_screen(self):
        return self.screen_manager.get_screen(self.screen_name)
