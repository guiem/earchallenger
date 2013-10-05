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
    submitted = []
    sol_count_notes = 0
    
    def _clear_buttons(self,buttons):
        for button in buttons:
            button.background_color = [1, 1, 1, 1]
            button.text = button.text.split('-')[0]

    def _reset_all(self,buttons):
        self.sequence = []
        self.submitted = []
        self.sol_count_notes = 0
        self.state = 'normal' # TODO: bind this?
        self._clear_buttons(buttons)
    
    def _check_answer(self):
        result = True
        if len(self.sequence) != len(self.submitted) or not self.sequence:
            result = False
        else:
            for i in range(0,len(self.sequence)-1):
                if self.sequence[i] != self.submitted[i]:
                    result = False
                    break
        return result
     
    def createScreens(self):
        self.screen_manager.add_widget(ChallengerScreen(name=self.screen_name, controller = self))
    
    def press_audio_btn(self,button):
        Logger.debug(_('ChallengerCtl: press_audio_btn'))
        if self.state == 'answering':
            self.submitted.append(button)
            self.sol_count_notes += 1
            button.background_color = [1,1,0,1]
            button.text = button.text + '-' + str(self.sol_count_notes)
        if button.sound.status != 'stop':
            button.sound.stop()
        button.sound.play()
     
    def play_sequence(self,buttons,num_notes):
        self.job_play_sequence = JobPlaySequence()
        self.job_play_sequence.controller=self
        self.job_play_sequence.start_job(buttons,num_notes,self.sequence)

    def play_next(self,buttons,num_notes):
        self._reset_all(buttons)
        self.job_play_sequence = JobPlaySequence()
        self.job_play_sequence.controller=self
        self.job_play_sequence.start_job(buttons,num_notes,self.sequence)
    
    def cancel(self,buttons):
        self._clear_buttons(buttons)
        self.submitted = []
        self.sol_count_notes = 0
     
    def answer(self):
        btn_label = ''
        feedback = ''
        if self.state == 'normal':
            self.state = 'answering'
            btn_label = _('Submit')
        elif self.state == 'answering':
            self.state = 'normal'
            btn_label = _('Answer')
            if self.sequence:
                correct = self._check_answer()
                if correct:
                    feedback = _('You are right!')
                else:
                    feedback = _('Sorry, you are wrong.')
            else:
                feedback = _('Sorry, you did not play any sequence.')
        return btn_label,feedback
     
    def show_solution(self,num_hints):
        num_to_show = num_hints + 1
        Logger.debug('ShowSolution: num_to_show '+str(num_to_show)+' len_seq '+str(len(self.sequence)))
        if self.sequence and num_to_show <= len(self.sequence):
            solution = []
            for note in self.sequence[:num_to_show]:
                solution.append(note.text)
            feedback = (',').join(solution)
            num_hints += 1
        else:
            feedback = _('Nothing has been played yet!')
            num_hints = 0
        return feedback,num_hints
         
    def prepareScreen(self):
        if not hasattr(self, 'screen'):
            self.screen = self.screen_manager.get_screen(self.screen_name)
            self.get_screen().prepare()

    def on_job_finished_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_finished')
        self.sequence = self.job_play_sequence.sequence
    
    def on_job_error_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_error')
    
    def on_feedback_init_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_feedback_init')

    def on_job_init_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_job_init')
        self.screen_manager.all_widgets_disabled=True
    
    def on_job_finally_play_sequence(self,sender):
        Logger.debug('ChallengerCtl: on_feedback_finally')
        self.screen_manager.all_widgets_disabled=False
    
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

