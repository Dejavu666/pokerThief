# GUI layer

# http://effbot.org/tkinterbook/frame.htm
# https://docs.python.org/3/library/tkinter.html#a-simple-hello-world-program



import tkinter, table
from tkinter.constants import *

tk = tkinter.Tk()
table = table.Table(4,1000,20)
for p in table.seat_order:
    table.plyr_dict[p].human = 1

frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2, width=1200)
frame.pack(expand=1)

title_label = tkinter.Label(frame,text='PokerMage')
title_label.pack(fill=X, expand=1)

pot_label = tkinter.Label(frame, text=str(table.pot))
pot_label.pack(fill=X, expand=1)

button = tkinter.Button(frame, text='start game',command=table.play_hand_loop)
button.pack(side=BOTTOM)

tk.mainloop()






# table = table.Table(4,1000,20)
# table.post_blinds()
# table.play_hand_loop()