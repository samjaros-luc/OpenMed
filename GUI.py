from tkinter import *
from PIL import ImageTk,Image

primary_color = ""
background_color = "#b81f1f"
contrast_color = "#ffffff"
global login_frame
global provider_menu
global find_patient
global display_patient
global edit_patient
global add_patient

window = Tk()   # create window
window.title("OpenMed")
window.iconbitmap("images/window_icon.ico")

background_image = ImageTk.PhotoImage(Image.open("images/rushing_ambulance.png"))
background_label = Label(window, image=background_image)
background_label.pack()

## Draw login area
def submitLogin(username, password):
    if username == "" or password == "":
        invalid = Label(login_frame, text="Username or password invalid")
        invalid.grid(row=1, column=0)
        return
    # TODO verify credentials
    login_frame.place_forget()
    paintProviderMenu()

def paintLogin():
    global login_frame
    login_frame = Frame(window, padx=50, pady=75, bg=background_color)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    program_name = Label(login_frame, text="OpenMed", fg=contrast_color, font=("Veranda", 36), pady=10, bg=background_color)
    program_name.grid(row=0, column=0)

    username_field = Entry(login_frame)
    username_field.grid(row=2, column=0)
    username_field.insert(0, "Username")

    password_field = Entry(login_frame)
    password_field.grid(row=3, column=0)
    password_field.insert(0, "Password")

    submit_button = Button(login_frame, text="Login", command=lambda: submitLogin(username_field.get(), password_field.get()))
    submit_button.grid(row=4, column=0)

def paintProviderMenu():
    global provider_menu
    provider_menu = Frame(window, padx=350, pady=275, bg=background_color)
    provider_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

    menu_name = Label(provider_menu, text="Provider Options", fg=contrast_color, font=("Veranda", 24), pady=20, bg=background_color)
    menu_name.grid(row=0, column=0)

    find_button = Button(provider_menu, text="Find Patient", bg=contrast_color, command=paintFindPatient)
    find_button.grid(row=1, column=0)

    add_button = Button(provider_menu, text="Add Patient", bg=contrast_color, command=paintAddPatient)
    add_button.grid(row=2, column=0)

def paintFindPatient():
    provider_menu.place_forget()
    global find_patient
    find_patient = Frame(window, padx=350, pady=275, bg=background_color)
    find_patient.place(relx=0.5, rely=0.5, anchor=CENTER)

    menu_name = Label(find_patient, text="Find a Patient", fg=contrast_color, font=("Veranda", 24), pady=20, bg=background_color)
    menu_name.grid(row=0, column=0, columnspan=2)

    first_name = Entry(find_patient)
    first_name.grid(row=1, column=0)
    first_name.insert(0, "First Name")

    last_name = Entry(find_patient)
    last_name.grid(row=1, column=1)
    last_name.insert(0, "Last Name")

    DOB = Entry(find_patient)
    DOB.grid(row=2, column=0)
    DOB.insert(0, "DOB")

    sex = Entry(find_patient)
    sex.grid(row=2, column=1)
    sex.insert(0, "Sex")

    type_selection = StringVar()
    type_selection.set("Diver's License")
    id_type = OptionMenu(find_patient, type_selection, "Driver's License", "ID Card", "Passport", "Green Card")
    id_type.grid(row=3, column=0)

    id_value = Entry(find_patient)
    id_value.grid(row=3, column=1)
    id_value.insert(0, "ID Value")

def paintDisplayPatient():
    return

def paintEditPatient():
    return

def paintAddPatient():
    return

paintLogin()
window.mainloop()
