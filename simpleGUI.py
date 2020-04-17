import PySimpleGUI as gui
from Database import Database
from Patient import Patient
from Medical_Event import Medical_Event

gui.ChangeLookAndFeel("Purple") # TODO Customize colors
gui.SetOptions(font=("Helvetica", 12), text_justification="center")
idTypes = ("Driver's License", "ID Card", "Passport", "Green Card")   # Possible ID types
dictPassthru = {}   # dictionary for passing through forms across pages
db = Database()   # Database object
global currentPatient   # Patient object being worked on


# Creates & operates login window
def login():
    loginbox = [
        [gui.T("Provider Login", font=("Helvetica", 16), justification="left")],
        [gui.T("Username")],
        [gui.In(key="user", justification="left")],
        [gui.T("Password")],
        [gui.In(password_char="*", key="pass", justification="left")],
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

        ################## REMOVE BEFORE TURNING IN ###########
        window.close()
        providerMenu()
        break

        if button is None:   # If X-out, break
            break

        usernameIn = values["user"]
        passwordIn = values["pass"]

        if db.userLogin(usernameIn, passwordIn):
            window.close()
            providerMenu()
            break
        else:
            gui.PopupError("Invalid username and/or password")


def providerMenu():
    global currentPatient

    col1 = [
        [gui.T("First Name")],
        [gui.In(key="first_name", do_not_clear=True, justification="left")],
        [gui.T("Last Name")],
        [gui.In(key="last_name", do_not_clear=True, justification="left")]
    ]
    col2 = [
        [gui.T("ID Type")],
        [gui.Combo(idTypes, key="id_type")],
        [gui.T("ID Value")],
        [gui.In(key="id_data", do_not_clear=True, justification="left")],
    ]

    layout = [
        [gui.T("Provider Menu", size=(30, 1), font=("Helvetica", 30), justification="center")],
        [gui.T("Patient Lookup", font=("Helvetica", 20))],
        [gui.T("_"*80, key="line")],
        [gui.Column(col1), gui.Column(col2)],
        [gui.Submit(), gui.Button("Create New Patient", enable_events=True)]
    ]

    window = gui.Window("OpenMed - Provider Menu", default_button_element_size=(40, 1)).Layout(layout)

    while True:
        button, values = window.Read()

        if button in (None, "Exit"):
            window.close()
            break
        elif button == "Create New Patient":
            window.close()
            newPatient(values)
        elif button == "Submit":
            currentPatient = db.get_patient(Patient(first_name=values["first_name"], last_name=values["last_name"],
                                                    id_type=values["id_type"], id_data=values["id_data"]).hashcode)
            if currentPatient is None:
                window["line"].update("Patient not found. Correct information or use Create New Patient button.")
            else:
                window.close()
                displayPatient()
                break

def newPatient(values):
    return   # TODO Write newPatient window


def displayPatient():
    global currentPatient

    col1 = [
        [gui.T("First Name:")],
        [gui.T("Last Name:")],
        [gui.T("ID Type:")],
        [gui.T("ID Value:")],
        [gui.T("Height:")],
        [gui.T("Weight:")],
        [gui.T("Sex:")],
        [gui.T("Date of Birth:")],
    ]
    col2 = [
        [gui.T(currentPatient.first_name)],
        [gui.T(currentPatient.last_name)],
        [gui.T(currentPatient.id_type)],
        [gui.T(currentPatient.id_data)],
        [gui.T(str(currentPatient.height))],
        [gui.T(str(currentPatient.weight))],
        [gui.T(currentPatient.sex)],
        [gui.T(currentPatient.dob)]
    ]
    med_events = []
    for event in currentPatient.med_events:
        start = [[gui.T("Start Date:")], [gui.T(str(event.start))]]
        end = [[gui.T("End Date:")], [gui.T(str(event.end))]]
        response = [[gui.T("Response:")], [gui.T(str(event.response))]]
        outcome = [[gui.T("Outcome:")], [gui.T(str(event.outcome))]]

        for drug in event.drugs:
            continue   # TODO create list of drug frames

        med_events.append(
            [gui.Frame(layout=[
                [gui.T(str(event.ICD10)+" - "+event.disease)],
                [gui.Column(start), gui.Column(end)],
                [gui.T("Symptoms:")],
                [gui.T(str(event.symptoms))],
                [gui.Frame(layout=[], title="Drugs")],
                [gui.Column(response), gui.Column(outcome)]
            ], title="")]
        )

    layout = [
        [gui.T("Patient View", size=(30, 1), font=("Helvetica", 30), justification="center")],
        [gui.Button("Edit This Patient", enable_events=True)],
        [gui.T(currentPatient.first_name+" "+currentPatient.last_name, font=("Helvetica", 20))],
        [gui.T("_"*80, key="line")],
        [gui.Frame(layout=[[gui.Column(col1), gui.Column(col2)]], title="Patient Info", size=(50, 50))],
        [gui.Frame(layout=med_events, title="Medical Events")],
        [gui.Button("Edit This Patient", enable_events=True)]
    ]

    window = gui.Window("OpenMed - "+currentPatient.last_name+", "+currentPatient.first_name,
                        default_button_element_size=(40, 1)).Layout(layout)

    while True:
        button, values = window.Read()

        if button == "Create New Patient":
            window.close()
            newPatient(values)
        elif button == "Submit":
            currentPatient = db.get_patient(Patient(first_name=values["first_name"], last_name=values["last_name"],
                                                    id_type=values["id_type"], id_data=values["id_data"]).hashcode)
            if currentPatient is None:
                window["line"].update("Patient not found. Correct information or use Create New Patient button.")
            else:
                displayPatient()
                window.close()


if __name__ == "__main__":
    login()
