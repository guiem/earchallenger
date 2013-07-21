#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kivy.app import App

def _(*args):
  return App.get_running_app().get_text(*args)
