#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils.job import Job
from utils.abstract_ctl import AbstractController
from challenger.challenger_view import ChallengerScreen
import traceback
from kivy.logger import Logger
from kivy.properties import StringProperty, ObjectProperty, ListProperty
import random
import time

class ChallengerCtl(AbstractController):
    screen_name='challenger'
      
    def play_sequence(self,buttons,num_notes,sequence):
        self.job_play_sequence = JobPlaySequence()
        self.job_play_sequence.controller=self
        self.job_play_sequence.start_job(buttons,num_notes,sequence)
    
    def createScreens(self):
        self.screen_manager.add_widget(ChallengerScreen(name=self.screen_name))

    def prepareScreen(self):
        screen =self.screen_manager.get_screen(self.screen_name)
        self.get_screen().prepare()

    def on_job_finished_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_finished')
        #self.user=self.job_login.user
        #self.user_data=self.job_login.user_data
        #menu_ctl.showScreen()
    def on_job_error_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_error')
    
    def on_feedback_init_login(self,sender):
        Logger.debug('ChallengerCtl: on_feedback_init')

    def on_job_init_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_init')
        #self.screen_manager.all_widgets_disabled=True
    
    def on_job_finally_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_feedback_finally')
        #self.screen_manager.all_widgets_disabled=False
    
    def on_feedback_loop_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: feedback_loop')
    
    def on_feedback_finished_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_feedback_finished')

class JobPlaySequence(Job):
    job_id='_play_sequence'
    
    def _create_sequence(self,buttons,num_notes):
        seq = []
        for i in range(num_notes):
            seq.append(buttons[random.randint(0,len(buttons)-1)])
        return seq
    
    def do_job(self,buttons,num_notes,sequence):
        Logger.debug('ChallengerCtl: do job '+str(sequence))
        if not sequence:
            sequence = self._create_sequence(buttons,num_notes)
        for btn in sequence:
            btn.sound.play()
            time.sleep(1) # TODO: check if there is a proper way to pause between sounds. Moreover: make speed adjustable by bar
            btn.sound.stop()

challenger_ctl=ChallengerCtl()

