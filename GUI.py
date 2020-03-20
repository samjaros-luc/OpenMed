from tkinter import *
from PIL import ImageTk,Image

primary_color = ""
background_color = "#f0c5c5"

window = Tk()   # create window
window.title("OpenMed")
window.iconbitmap("images/window_icon.ico")

background_image = ImageTk.PhotoImage(Image.open("images/rushing_ambulance.png"))
background_label = Label(window, image=background_image)
background_label.pack()

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

login_frame = Frame(window, padx=100, pady= 150, bg=background_color)
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

program_name = Label(login_frame, text="OpenMed", fg="white", font=("Veranda", 36), pady=10)
program_name.grid(row=0, column=0)

username_field = Entry(login_frame)
username_field.grid(row=1,column=0)
username_field.insert(0, "Username")

password_field = Entry(login_frame)
password_field.grid(row=2,column=0)
password_field.insert(0, "Password")

submit_button = Button(login_frame, text="Login")
submit_button.grid(row=3,column=0)

window.mainloop()
