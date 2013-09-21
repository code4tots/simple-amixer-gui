#!/usr/bin/python
'''
Should be compatible with both Python 2 and 3.
From what I understand, the only issue is the tkinter package name.
'''
import sys
from os import popen

if sys.version_info >= (3,0):
  from tkinter import *
else:
  from Tkinter import *

'''
callbacks
'''
def on_new_scale_value(v):
  popen('amixer -c 0 set Master %s' % v).read()

def on_mouse_wheel(event):
  if event.num == 5 or event.delta == -120:
    value.set(value.get()-1)
  if event.num == 4 or event.delta ==  120:
    value.set(value.get()+1)
  on_new_scale_value(value.get())

'''
get amixer data
'''
def cmd(c):
  '''
  Call system command specified by 'c' and return output stripping whitespace.
  '''
  return popen(c).read().strip()

start = int(cmd(
    r"""amixer get Master |
        grep -m 1 -o 'Playback [0-9][0-9]* \[[0-9][0-9]*\%\]' | \
        grep -m 1 -o '[0-9][0-9]*'""").split()[0])

low, high   = map(int,cmd(
  r"""amixer get Master | \
      grep -m 1 -o 'Limits: Playback [0-9][0-9]* \- [0-9][0-9]*' | \
      grep -m 2 -o '[0-9][0-9]*'""").split())

'''
Setup Tkinter
'''
root  = Tk()
value = DoubleVar()
value.set(start)
scale = Scale(root,
              variable = value,
              command = on_new_scale_value,
              from_=low,
              to=high,
              width=15,
              length=200)
scale.pack(anchor=CENTER)

'''
Windows throws <MouseWheel> events,
Linux   throws <Button-4> and <Button-5> events

However, it probably is silly adding Windows support here, because I'm pretty
sure that Windows doesn't use alsamixer or grep.

Maybe it can just be reference if I want to create another Python Tkinter 
script with mouse scrolls.
'''
root.bind("<MouseWheel>", on_mouse_wheel)
root.bind("<Button-4>", on_mouse_wheel)
root.bind("<Button-5>", on_mouse_wheel)

'''
Set window to upper right corner,
and dimension of the root window.
'''
root.geometry('60x200-0+0')
root.wm_title('simple_amixer_gui')

root.mainloop()
