import PySimpleGUI as gui

gui.ChangeLookAndFeel("Purple") # TODO Customize colors
gui.SetOptions(font=("Helvetica", 12), text_justification="center")
idTypes = ("Driver's License", "ID Card", "Passport", "Green Card")   # Possible ID types
dictPassthru = {}   # dictionary for passing through forms across pages

# Creates & operates login window
def login():
    loginbox = [
        [gui.T("Provider Login", font=("Helvetica", 16), justification="left")],
        [gui.T("Username")],
        [gui.In(key="user")],
        [gui.T("Password")],
        [gui.In(password_char="*", key="pass")],
        [gui.Submit()]
    ]

    layout = [
        [gui.T("OpenMed", font=("Helvetica", 30), justification="center")],
        [gui.T("Secure medical records available when you need them", font=("Helvetica", 20), justification="center")],
        [gui.Column(loginbox, justification="center")]
    ]

    window = gui.Window("OpenMed - Login", default_button_element_size=(40, 1)).Layout(layout)
    # Loop keeps login window open until X-out or a valid login is made
    while True:
        button, values = window.Read()

        if button is None:   # If X-out, break
            break

        usernameIn = values["user"]
        passwordIn = values["pass"]

        if usernameIn == "samjaros" and passwordIn == "password":
            window.close()
            providerMenu()
        else:
            gui.PopupError("Invalid username and/or password")


def providerMenu():
    col1 = [
        [gui.T("First Name")],
        [gui.In(key="fn", do_not_clear=True)],
        [gui.T("ID Type")],
        [gui.In(key="IDtype", do_not_clear=True)]
    ]
    col2 = [
        [gui.T("Last Name")],
        [gui.In(key="ln", do_not_clear=True)],
        [gui.T("ID Value")],
        [gui.In(key="IDval", do_not_clear=True)],
    ]

    layout = [
        [gui.T("Provider Menu", size=(30, 1), font=("Helvetica", 30), justification="center")],
        [gui.T("Patient Lookup", font=("Helvetica", 20))],
        [gui.T("_"*80)],
        [gui.Column(col1), gui.Column(col2)],
        [gui.Submit(), gui.Button("Create New Patient", enable_events=True)]
    ]

    window = gui.Window("OpenMed - Provider Menu", default_button_element_size=(40, 1)).Layout(layout)
    button, values = window.Read()

    if button == "Create New Patient":
        window.close()
        newPatient(values)
    elif button == "Submit":
        return   # TODO lookup patient using hash


def newPatient(values):
    return   # TODO Write newPatient window


def displayPatient(Patient):
    return   # TODO Write displayPatient window


if __name__ == "__main__":
    login()
