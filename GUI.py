from tkinter import *

window = Tk()   # create window
window.title("OpenMed")
window.iconphoto(True, PhotoImage(file="C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/images/window_icon.png"))

background_image = PhotoImage(file="C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/images/rushing_ambulance.png")
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

window.mainloop()
