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
from utils.i18n import _

class ChallengerCtl(AbstractController):
    screen_name='challenger'
    state = StringProperty('normal')
    sequence = []
    
    def createScreens(self):
        self.screen_manager.add_widget(ChallengerScreen(name=self.screen_name, controller = self))
    
    def play_sequence(self,buttons,num_notes):
        self.job_play_sequence = JobPlaySequence()
        self.job_play_sequence.controller=self
        self.job_play_sequence.start_job(buttons,num_notes,self.sequence)

    def play_next(self,buttons,num_notes):
        self.sequence = []
        self.job_play_sequence = JobPlaySequence()
        self.job_play_sequence.controller=self
        self.job_play_sequence.start_job(buttons,num_notes,self.sequence)
   
    def answer(self):
        btn_label = ''
        if self.state == 'normal':
            self.state = 'answering'
            btn_label = _('Submit')
        elif self.state == 'answering':
            self.state = 'normal'
            btn_label = _('Answer')
        return btn_label
     
    def show_solution(self,solution):
        res = _('Nothing has been played yet!')
        if self.sequence:
            solution = []
            for note in self.sequence:
                solution.append(note.text)
            res = (',').join(solution)
        return res
         
    def prepareScreen(self):
        screen =self.screen_manager.get_screen(self.screen_name)
        self.get_screen().prepare()

    def on_job_finished_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_finished')
        self.sequence = self.job_play_sequence.sequence
    
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
    sequence = []
     
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
            time.sleep(1) # TODO: Moreover: make speed adjustable by bar
            btn.sound.stop()
        self.sequence = sequence
        self.job_state  = 'finished'

challenger_ctl=ChallengerCtl()

