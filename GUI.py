from tkinter import *

window = Tk()   # create window

## Put some text in the window
title = Label(window, text="This is my window")
title.pack()   # put the text wherever it fits in the window

## Invisible frame
topFrame = Frame(window)
topFrame.pack(side=TOP)   # parameter not really necessary
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)

## Make a button
button1 = Button(topFrame, text="Button 1", fg="red")
button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Button 4", fg="purple")

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)

window.mainloop()
