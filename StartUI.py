#UI
#Xiaoyi(Sean) Wang
#2018-8-16

import tkinter as tk
import ImageCap as IC
window = tk.Tk()
window.title('my window')
window.geometry('250x250')

var = tk.StringVar()
var.set('SmartI')

var1 = tk.IntVar()

l1 = tk.Label(window, textvariable=var,bg='grey',font=('Arial',20),width=30,height=2)
l1.pack()

r1 = tk.Radiobutton(window,text='Internal Camera', variable=var1,value=0)
r1.pack()
r1 = tk.Radiobutton(window,text='USB Camera', variable=var1,value=1)
r1.pack()


print(var1)

on_hit = False
def TrainingButton():
	global on_hit
	if on_hit == False:
		on_hit = True
		var.set('click to start, press q to stop')
	else:
		on_hit = False
		var.set('Sample collecting')
		IC.frameRun(var1.get())


b = tk.Button(window, text='Sample Collection', width=15,height=2,command=TrainingButton)
b.pack()

b1 = tk.Button(window, text='Sample Training', width=15,height=2,command=TrainingButton)
b1.pack()

b2 = tk.Button(window, text='Testing', width=15,height=2,command=TrainingButton)
b2.pack()

b3 = tk.Button(window, text='Run', width=15,height=2,command=TrainingButton)
b3.pack()


window.mainloop()

