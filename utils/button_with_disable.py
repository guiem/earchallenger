#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.logger import Logger

class ButtonWithDisable(Button):
    activeColor = ListProperty([1,1,1,1])
    inactiveColor = ListProperty([1,1,1,.25])
    active = BooleanProperty(True)
    
    def __init__(self,*args,**kwargs):
        super(ButtonWithDisable,self).__init__(*args,**kwargs)
    
    def on_active(self,who,what):
        if (what):
            self.color=self.activeColor
        else:
            self.color=self.inactiveColor
    
    def on_touch_down(self,touch):
        if (self.active):
            return super(ButtonWithDisable,self).on_touch_down(touch)


