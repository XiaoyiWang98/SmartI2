import sys
import ImageCap as ic
sys.path.insert(0, 'MouthDetector')
import MouthDetection2 as md
import train_model
import FramePredict as fp

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from train_model import train_model
from validate_model import validate_model

class EyeCollect(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = FloatLayout(size=(500,300))
        layout.add_widget(
        Label(
            text='Welcome to SmartI',
            pos_hint={'x': 0, 'center_y': .55},
            font_size='40sp'
            ))
        self.countdown = Label(
            id = 'countdown',
            text='Starting Eye Sample Collection in 10 Seconds',
            pos_hint={'x': 0, 'center_y': .4},
            font_size='20sp'
            )
        layout.add_widget(self.countdown)
        self.add_widget(layout)

        self.time = 10
        Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        if self.time == 0:
            ic.frameRun(0)
            Clock.unschedule(self.update)
            self.manager.current = 'mouthcollect'
        self.time = self.time - 1
        self.countdown.text = str('Starting Eye Sample Collection in ' + str(self.time) + ' Seconds')
        

class MouthCollect(Screen):

    def on_enter(self):
        self.clear_widgets()
        layout = FloatLayout(size=(500,300))
        self.countdown = Label(
            id = 'countdown',
            text='Starting Mouth Sample Collection in 10 Seconds',
            pos_hint={'x': 0, 'center_y': .5},
            font_size='20sp'
            )
        layout.add_widget(self.countdown)
        self.add_widget(layout)
        self.time = 10
        Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        if self.time == 0:
            md.frameRun2(0)
            Clock.unschedule(self.update)
            self.manager.current = 'trainscreen'
        self.time = self.time - 1
        self.countdown.text = str('Starting Mouth Sample Collection in ' + str(self.time) + ' Seconds')

class TrainScreen(Screen):

    def on_enter(self):
        self.clear_widgets()
        layout = FloatLayout(size=(500,300))
        layout.add_widget(
        Label(
            text='Training and Validating...',
            pos_hint={'x': 0, 'center_y': .55},
            font_size='30sp'
            ))
        layout.add_widget(
        Label(
            text='(May Take a While)',
            pos_hint={'x': 0, 'center_y': .45},
            font_size='20sp'
            ))
        self.add_widget(layout)
        Clock.schedule_interval(self.train, 1)

    def train(self, dt):
        Clock.unschedule(self.train)
        train_model(90, 1, 4) 
        train_model(90, 1, 2) 
        self.eyeAccuracy = validate_model(90, 0, 4)
        self.mouthAccuracy = validate_model(90, 0, 2)

        if (self.eyeAccuracy < 80) or (self.mouthAccuracy < 80) :
            failLayout = FloatLayout(size=(500,300))
            self.countdown = Label(
                id = 'countdown',
                text='Failed, Collecting New Samples in 5 Seconds',
                pos_hint={'x': 0, 'center_y': .5},
                font_size='20sp'
            )
            failLayout.add_widget(self.countdown)
            self.clear_widgets()
            self.add_widget(failLayout)
            self.time = 5
            Clock.schedule_interval(self.update, 1)
        else:
            self.manager.current = 'smartcontrol'

    def update(self, dt):
        if self.time == 0:
            Clock.unschedule(self.update)
            self.manager.current = 'eyecollect'
        self.time = self.time - 1
        self.countdown.text = str('Failed, Collecting New Samples in ' + str(self.time) + ' Seconds')

class SmartControl(Screen):

    def on_enter(self):
        #Initial Screen Layout
        layout = FloatLayout(size=(500,300))
        layout.add_widget(
        Label(
            text='Running SmartI...',
            pos_hint={'x': 0, 'center_y': .55},
            font_size='30sp'
            ))
        self.add_widget(layout)
        Clock.schedule_interval(self.update, 1) 
    
    def update(self, dt):
        Clock.unschedule(self.update)
        fp.framePredict(0)
        

class SmartI(App):
    def build(self):
        # Config Window
        Window.size = (500, 300)
        Window.clearcolor = get_color_from_hex('#2a3551')
        # Add Screens
        sm = ScreenManager()
        sm.add_widget(EyeCollect(name='eyecollect'))
        sm.add_widget(MouthCollect(name='mouthcollect'))
        sm.add_widget(TrainScreen(name='trainscreen'))
        sm.add_widget(SmartControl(name='smartcontrol'))
        return sm

if __name__ == '__main__':
    SmartI().run()
