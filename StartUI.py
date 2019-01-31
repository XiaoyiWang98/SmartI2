#UI
#Xiaoyi(Sean) Wang
#2018-8-16

import tkinter as tk
import ImageCap as IC
import sys
sys.path.insert(0, 'MouthDetector')
import MouthDetection2 as MD
import train_model
from train_model import train_model
from validate_model import validate_model
import time


window = tk.Tk()
window.title('my window')
window.geometry('300x400')

var = tk.StringVar()
var.set('SmartI')

var1 = tk.IntVar()

l1 = tk.Label(window, textvariable=var,bg='grey',font=('Arial',20),width=30,height=2)
l1.pack()

r1 = tk.Radiobutton(window,text='Internal Camera', variable=var1,value=0)
r1.pack()
r1 = tk.Radiobutton(window,text='USB Camera', variable=var1,value=1)
r1.pack()

percent = 90  # percent = % of training data in the dataset

print(var1)

on_hit = False
def SampleCollectionButton():
  global on_hit
  if on_hit == False:
    on_hit = True
    var.set('click to start, press q to stop')
  else:
    on_hit = False
    var.set('Sample collecting')
    IC.frameRun(var1.get())

def SampleCollectionButton2():
  global on_hit
  if on_hit == False:
    on_hit = True
    var.set('click to start, press q to stop')
  else:
    on_hit = False
    var.set('Sample collecting')
    MD.frameRun2(var1.get())

def TrainingButton():
  start = time.time()

  #train_model(percent, 1, 4)  # for eyes
  train_model(percent, 1, 2)  # for mouth

  end = time.time()
  #print(end - start)

def TestButton():
  start = time.time()

  print(validate_model(percent, 0, 4))  # for eyes
  #validate_model(percent, 0, 2)  # for mouth

  end = time.time()
  #print(end - start)

b = tk.Button(window, text='Eye Sample Collection', width=30,height=2,command=SampleCollectionButton)
b.pack()

b4 = tk.Button(window, text='Mouth Sample Collection', width=30,height=2,command=SampleCollectionButton2)
b4.pack()

b1 = tk.Button(window, text='Sample Training', width=30,height=2,command=TrainingButton)
b1.pack()

b2 = tk.Button(window, text='Testing', width=30,height=2,command=TestButton)
b2.pack()

b3 = tk.Button(window, text='Run', width=30,height=2,command=SampleCollectionButton)
b3.pack()


window.mainloop()

