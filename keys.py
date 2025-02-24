"""
This file is impl tkinter library,
no unittest only impl test
"""

from tkinter import *
import os
import threading
import time
import lcm
from exlcm import twist_t

class Keyboard:
    def __init__(self):
        self.lc = lcm.LCM()
        self.key_whitelist = {25,38,39,40,65,54}
        self.status_dct = {}
        self.key_dct = {}
        os.system('xset r off')
        self.frame = Tk()
        self.frame.geometry('750x300')
        self.frame.title("URC 2025 Ground Station")
        self.frame.bind("<KeyPress>", self.keydown)
        self.frame.bind("<KeyRelease>", self.keyup)
        self.speed = float(1.0)
        # self.frame.pack()
        self.config()
        self.msg = twist_t()
        self.msg.linear = (0.0,0.0,0.0)
        self.msg.angular = (0.0,0.0,0.0)
        self.frame.focus_set()
        self.frame.mainloop()

    def config(self):
        self.movement_lbl = Label(self.frame, text="Movement: ")
        self.movement_lbl.grid(column=0, row=0)
        self.prompt_lbl = Label(self.frame, text="enter target speed")
        self.prompt_lbl.grid(column=0, row=1)
        self.txt = Entry(self.frame,width=10)
        self.txt.grid(column=1, row=1)
        self.btn = Button(self.frame, text="Set", command=self.clicked)
        self.btn.grid(column=2, row=1)
        self.speed_lbl = Label(self.frame, text="Odrive Speed is set to ")
        self.speed_lbl.grid(column=0, row=2)
        self.odrive_prompt_lbl = Label(self.frame, text="enter odrive cmd(value based)")
        self.odrive_prompt_lbl.grid(column=0, row=3)
        self.axis_lbl = Label(self.frame, text=" axis:")
        self.axis_lbl.grid(column=0, row=4)
        self.axis_txt = Entry(self.frame,width=10)
        self.axis_txt.grid(column=1, row=4)
        self.cmd_lbl = Label(self.frame, text=" cmd:")
        self.cmd_lbl.grid(column=2, row=4)
        self.cmd_txt = Entry(self.frame,width=10)
        self.cmd_txt.grid(column=3, row=4)
        self.value_lbl = Label(self.frame, text=" value(optional):")
        self.value_lbl.grid(column=4, row=4)
        self.value_txt = Entry(self.frame,width=10)
        self.value_txt.grid(column=5, row=4)
        self.btn = Button(self.frame, text="Set", command=self.odrive_clicked)
        self.btn.grid(column=6, row=4)
        self.odrive_cmd_lbl = Label(self.frame, text="")
        self.odrive_cmd_lbl.grid(column=0, row=5)
            
    def keydown(self, e):
        if e.keycode in self.key_whitelist:
            if e.char == 'w':
                self.msg.linear = (self.speed,0.0,0.0)
            if e.char == 's':
                self.msg.linear = (-self.speed,0.0,0.0)
            if e.char == 'a':
                self.msg.angular = (0.0,0.0,self.speed*0.25)
            if e.char == 'd':
                self.msg.angular = (0.0,0.0,-self.speed*0.25)
            print(self.msg.linear, ' ', self.msg.angular)
            self.lc.publish("control", self.msg.encode())
            print (f'down {e.char}')
            if e.keycode not in self.status_dct:
                self.key_dct[e.keycode] = e.char
            self.status_dct[e.keycode] = True
            keys = list(self.key_dct[code] for code in self.status_dct if self.status_dct[code] is True)
            res = 'Movement: ' + "".join(keys)
            self.movement_lbl.configure(text= res)
        
    def keyup(self, e):
        if e.keycode in self.key_whitelist:
            if self.key_dct[e.keycode] == 'w' or self.key_dct[e.keycode] == 's':
                self.msg.linear = (0.0,0.0,0.0)
            if self.key_dct[e.keycode] == 'a' or self.key_dct[e.keycode] == 'd':
                self.msg.angular = (0.0,0.0,0.0)
            print(self.msg.linear, ' ', self.msg.angular)
            self.lc.publish("control", self.msg.encode())
            print (f'up {self.key_dct[e.keycode]}')
            self.status_dct[e.keycode] = False
            keys = list(self.key_dct[code] for code in self.status_dct if self.status_dct[code] is True)
            res = 'Movement: ' + "".join(keys)
            self.movement_lbl.configure(text= res)
        
    def clicked(self):
        res = 'Odrive Speed is set to ' + str(self.txt.get())
        self.speed = float(self.txt.get())
        self.speed_lbl.configure(text= res)
        
    def odrive_clicked(self):
        res = str(self.axis_txt.get()) + ' ' + str(self.cmd_txt.get()) + ' ' + str(self.value_txt.get())
        self.odrive_cmd_lbl.configure(text= res)    
            
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.system('xset r on')

Keyboard()