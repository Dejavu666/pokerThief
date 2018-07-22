# GUI layer

# http://effbot.org/tkinterbook/frame.htm
# https://docs.python.org/3/library/tkinter.html#a-simple-hello-world-program



import tkinter, table
from tkinter.constants import *

tk = tkinter.Tk()
table = table.Table(4,1000,20)

frame = tkinter.Frame(tk, relief=RIDGE,borderwidth=2)
frame.pack(fill=BOTH, expand=1)

label = tkinter.Label(frame,text='hello mars')
label.pack(fill=X, expand=1)

button = tkinter.Button(frame, text='start game',command=table.play_hand_loop)
button.pack(side=BOTTOM)

tk.mainloop()






# table = table.Table(4,1000,20)
# table.post_blinds()
# table.play_hand_loop()