# GUI layer

# tkinter i guess for now
# hello mars
# import tkinter
# from tkinter.constants import *
# tk = tkinter.Tk()
# frame = tkinter.Frame(tk, relief=RIDGE,borderwidth=2)
# frame.pack(fill=BOTH, expand=1)
# label = tkinter.Label(frame,text='hello mars')
# label.pack(fill=X, expand=1)
# button = tkinter.Button(frame, text='exit',command=tk.destroy)
# button.pack(side=BOTTOM)
# tk.mainloop()



import table

table = table.Table(4,1000,20)
table.post_blinds()
table.play_hand_loop()