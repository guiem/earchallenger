#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from utils.i18n import _
from kivy.properties import ObjectProperty
from utils.abstract_ctl import AbstractController

from kivy.lang import Builder
Builder.load_file('utils/info.kv')

class ErrorLayout(BoxLayout):
    lbl=ObjectProperty(None)
    trace=ObjectProperty(None)
    btn=ObjectProperty(None)
    sc=ObjectProperty(None)
   
    def show_hide_trace(self):
        if self.sc.size[1] == 0:
            self.sc.size = (self.sc.size[0],150)
        else:
            self.sc.size = (self.sc.size[0],0) 



class InfoCtl(AbstractController):
    def error(self,titol,msg,trace):
        e=ErrorLayout()
        e.lbl.text=msg
        e.trace.text = trace
        e.btn.text=_('Aceptar')
        popup = Popup(title=titol,
                      content=e,
                      size_hint=(None, None), size=(400, 400))
        e.btn.bind(on_press=popup.dismiss)
        popup.open()
    def createScreens(self):
        pass
    

info_ctl=InfoCtl()
