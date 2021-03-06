#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils.job import Job
from utils.abstract_ctl import AbstractController
from utils.database_manager import EarChallengerDB
from challenger.challenger_view import ChallengerScreen
import traceback
from kivy.logger import Logger
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
import random
import time
from utils.i18n import _

class ChallengerCtl(AbstractController):
    screen_name='challenger'
    state = StringProperty('normal')
    sequence = []
    submitted = []
    sol_count_notes = 0
    num_notes = NumericProperty(5)
    
    def change_num_notes(self, num_notes):
        if num_notes != self.num_notes:
            self.num_notes = num_notes
            self.sequence = []
    
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
     
    def play_sequence(self,buttons):
        self.job_play_sequence = JobPlaySequence()
        self.job_play_sequence.controller=self
        self.job_play_sequence.start_job(buttons,self.num_notes,self.sequence)
        self.screen.played_times += 1

    def next_sequence(self,buttons,feedback=False):
        dbmgr = EarChallengerDB()
        correct = 1 if self._check_answer() else 0
        dbmgr.insert_stat(correct,self.screen.played_times,self.screen.hints,self.num_notes,'alto_sax','todo:put sequence here',5)
        self.screen.played_times = 0
        self.screen.hints = 0
        # TODO: show it in a dialog
        if not feedback:
            feedback = _('New sequence available, press Play!')
        self.screen.solution = feedback
        self._reset_all(buttons)
    
    def skip(self,buttons):
        solution = self.get_solution_str()
        feedback = False if not solution else _('The solution was: %s' %(solution,))
        self.next_sequence(buttons,feedback=feedback)
    
    def cancel(self,buttons):
        self._clear_buttons(buttons)
        self.submitted = []
        self.sol_count_notes = 0
     
    def answer(self,buttons):
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
                feedback = _('Sorry, you did not even play any sequence.')
            self.next_sequence(buttons)
        return btn_label,feedback

    def get_solution_str(self):
        return (',').join([note.text for note in self.sequence])
    
    def show_hint(self):
        feedback = (',').join([note.text for note in self.sequence[:self.screen.hints+1]])
        self.screen.solution = feedback
        if self.screen.hints < len(self.sequence):
            self.screen.hints += 1
    
    def prepareScreen(self):
        if not hasattr(self, 'screen'):
            self.screen = self.screen_manager.get_screen(self.screen_name)
            self.get_screen().prepare()
        # TODO: done by sqlite now because storage is not present in Kivy 1.7.2
        #from kivy.storage.jsonstore import JsonStore
        #store = JsonStore('settings.json')
        #if store:
        #    self.change_num_notes(store.get('num_notes')['value'])
        dbmgr = EarChallengerDB()
        num_notes = dbmgr.get_setting("num_notes")
        if num_notes != None:
            self.change_num_notes(num_notes)

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

