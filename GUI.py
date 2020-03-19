from tkinter import *

window = Tk()   # create window
window.title("OpenMed")
window.iconphoto(True, PhotoImage(file="C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/images/window_icon.png"))

background_image = PhotoImage(file="C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/images/rushing_ambulance.png")
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

## Draw login area
def submitLogin():
    username = username_field.get()
    password = password_field.get()
    if username == "" or password == "":
        invalid = Label(login_frame, text="Username or password invalid")
        invalid.pack(side=TOP)
        return
    # TODO verify credentials
    # go to next page

login_frame = Frame(window, bg="#f0c5c5")
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

username_field = Entry(login_frame)
username_field.pack()
username_field.insert(0, "Username")

password_field = Entry(login_frame)
password_field.pack()
password_field.insert(0, "Password")

submit_button = Button(login_frame, text="Login")
submit_button.pack()

window.mainloop()
