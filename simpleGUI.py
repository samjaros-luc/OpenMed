import PySimpleGUI as gui
from Database import Database
from Patient import Patient
from Medical_Event import Medical_Event
from datetime import date

gui.ChangeLookAndFeel("Purple") # TODO Customize colors
gui.SetOptions(font=("Helvetica", 12))
idTypes = ("Driver's License", "ID Card", "Passport", "Green Card")   # Possible ID types
sexOptions = ("Female", "Male", "Unknown")   # Possible sexes
db = Database()   # Database object
windowName = "login"

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

        if button in (None, "Quit"):   # If X-out, break
            window.close()
            break

        ################## REMOVE BEFORE TURNING IN ###########
        window.close()
        providerMenu()
        break

        usernameIn = values["user"]
        passwordIn = values["pass"]

        if db.userLogin(usernameIn, passwordIn):
            window.close()
            providerMenu()
            break
        else:
            gui.PopupError("Invalid username and/or password")


# After login, provides provider window which can search for a patient or create a new patient
def providerMenu():
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

    window = gui.Window("OpenMed - Provider Menu", resizable=True).Layout(layout)

    while True:
        button, values = window.Read()

        if button in (None, "Quit"):
            window.close()
            break
        elif button == "Create New Patient":
            window.close()
            editPatientInfo(Patient(first_name=values["first_name"], last_name=values["last_name"],
                                id_type=values["id_type"], id_data=values["id_data"]))
            break
        elif button == "Submit":
            currentPatient = db.get_patient(Patient(first_name=values["first_name"], last_name=values["last_name"],
                                                    id_type=values["id_type"], id_data=values["id_data"]).hashcode)
            if currentPatient is None:
                window["line"].update("Patient not found. Correct information or use Create New Patient button.")
            else:
                window.close()
                displayPatient(currentPatient)
                break


def displayPatient(patient: Patient):
    col1 = [
        [gui.T("First Name:")],
        [gui.T("Last Name:")],
        [gui.T("ID Type:")],
        [gui.T("ID Value:")],
        [gui.T("Height:")],
        [gui.T("Weight:")],
        [gui.T("Sex:")],
        [gui.T("Date of Birth:")]
    ]

    col2 = [
        [gui.T(patient.first_name)],
        [gui.T(patient.last_name)],
        [gui.T(patient.id_type)],
        [gui.T(patient.id_data)],
        [gui.T(str(patient.height))],
        [gui.T(str(patient.weight))],
        [gui.T(patient.sex)],
        [gui.T(str(patient.dob))]
    ]

    med_events = []
    for event in patient.med_events:
        drugs = []
        for drug in event.drugs:
            start = [[gui.T("Start Date:")], [gui.T(str(drug.start))]]
            end = [[gui.T("End Date:")], [gui.T(str(drug.end))]]

            assembled_name = drug.name+" ("+drug.generic_name+")" if drug.name != "" and drug.generic_name != "" \
                             else drug.generic_name if drug.name == "" \
                             else drug.name

            drugs.append(
                [gui.Frame(layout=[
                    [gui.T(assembled_name+" - "+drug.dosage)],
                    [gui.Column(start), gui.Column(end)],
                    [gui.T("Side Effects:")],
                    [gui.T(str(drug.side_effects))],
                    [gui.T("Incompatible Drugs:")],
                    [gui.T(str(drug.incompatible_drugs))]
                ], title="")]
            )

        start = [[gui.T("Start Date:")], [gui.T(str(event.start))]]
        end = [[gui.T("End Date:")], [gui.T(str(event.end))]]
        response = [[gui.T("Response:")], [gui.T(str(event.response))]]
        outcome = [[gui.T("Outcome:")], [gui.T(str(event.outcome))]]

        med_events.append(
            gui.Frame(layout=[
                [gui.T(event.disease+" ("+event.ICD10+")")],
                [gui.Column(start), gui.Column(end)],
                [gui.T("Symptoms:")],
                [gui.T(str(event.symptoms))],
                [gui.Frame(layout=drugs, title="Drugs")],
                [gui.Column(response), gui.Column(outcome)],
                [gui.Button("Edit Medical Event")]
            ], title="")
        )

    layout = [
        [gui.T(patient.first_name+" "+patient.last_name, size=(30, 1), font=("Helvetica", 30), justification="center")],
        [gui.T("_"*80, key="line", justification="center")],
        [gui.Frame("Patient Info", layout=[[gui.Column(col1), gui.Column(col2)],
                                           [gui.Button("Edit Patient Info", key="P"+patient.hashcode, enable_events=True)]]),
         gui.Frame("Medical Events", layout=[[gui.Button("Add Medical Event", key="M", enable_events=True)],
                                             med_events])],
        [gui.Button("Return to Provider Menu", enable_events=True)]
    ]

    window = gui.Window("OpenMed - "+patient.last_name+", "+patient.first_name, resizable=True).Layout(layout)

    while True:
        button, values = window.Read()

        if button in (None, "Quit"):
            window.close()
            break
        if button == "Return to Provider Menu":
            window.close()
            providerMenu()
            break
        if button == "Edit Patient Info":
            window.close()
            editPatientInfo(patient)
            displayPatient(patient)
            break
        if button[0] == "M":
            hashcode = button[1:]
            editMedicalEvent(patient, hashcode)


# Given a patient, creates a popup window that allows for the editing of the basic information in the Patient class
def editPatientInfo(patient: Patient):
    labels = [
        [gui.T("First Name:")],
        [gui.T("Last Name:")],
        [gui.T("ID Type:")],
        [gui.T("ID Value:")],
        [gui.T("Height:")],
        [gui.T("Weight:")],
        [gui.T("Sex:")],
        [gui.T("Date of Birth:")]
    ]
    inputs = [
        [gui.In(patient.first_name, key="first_name", size=(17, 1))],
        [gui.In(patient.last_name, key="last_name", size=(15, 1))],
        [gui.InputCombo(idTypes, default_value=patient.id_type, key="id_type", size=(15, 1))],
        [gui.In(patient.id_data, key="id_data", size=(15, 1))],
        [gui.In(str(patient.height), key="height", size=(15, 1))],
        [gui.In(str(patient.weight), key="weight", size=(15, 1))],
        [gui.InputCombo(sexOptions, default_value=patient.sex, key="sex", size=(15, 1))],
        [gui.In(str(patient.dob), key="dob", size=(9, 1), pad=(2,0)),
         gui.CalendarButton("", target="dob", image_filename="images/calendar.png", image_subsample=18)]
    ]

    layout = [
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Submit()]
    ]

    window = gui.Window("Edit Patient Info").Layout(layout)

    button, values = window.Read()
    patient.first_name = values["first_name"]
    patient.last_name = values["last_name"]
    patient.id_type = values["id_type"]
    patient.id_data = values["id_data"]
    patient.height = values["height"]
    patient.weight = values["weight"]
    patient.sex = values["sex"]
    if len(values["dob"]) >= 10:
        patient.dob = date.fromisoformat(values["dob"][:10])
    else:
        patient.dob = None
    print(str(patient.dob))
    db.push_patient(patient)


# Given a patient and a hash of a Medical Event, creates a popup window that allows for the editing of the information
# in the Medical_Event class
def editMedicalEvent(patient: Patient, hashcode: str = ""):
    event = None
    for e in patient.med_events:
        if hashcode == e.hashcode:
            event = e
    if event is None:
        event = Medical_Event(patient=patient.hashcode)

    drugs = []
    for drug in event.drugs:
        start = [[gui.T("Start Date:")], [gui.T(str(drug.start))]]
        end = [[gui.T("End Date:")], [gui.T(str(drug.end))]]

        assembled_name = drug.name+" ("+drug.generic_name+")" if drug.name != "" and drug.generic_name != "" \
            else drug.generic_name if drug.name == "" \
            else drug.name

        drugs.append(
            [gui.Frame(layout=[
                [gui.T(assembled_name+" - "+drug.dosage)],
                [gui.Column(start), gui.Column(end)],
                [gui.T("Side Effects:")],
                [gui.T(str(drug.side_effects))],
                [gui.T("Incompatible Drugs:")],
                [gui.T(str(drug.incompatible_drugs))]
            ], title="")]
        )

    symps = ""
    for s in event.symptoms:
        symps = symps + s + "\n"

    labels = [
        [gui.T("ICD10:")],
        [gui.T("Disease:")],
        [gui.T("Response:")],
        [gui.T("Outcome:")],
        [gui.T("Start:")],
        [gui.T("End:")],
        [gui.T("Symptoms:")],
    ]
    inputs = [
        [gui.In(event.ICD10, key="ICD10", size=(15, 1))],
        [gui.In(event.disease, key="disease", size=(15, 1))],
        [gui.In(event.response, key="response", size=(15, 1))],
        [gui.In(event.outcome, key="outcome", size=(15, 1))],
        [gui.In(str(event.start), key="start", size=(15, 1)),
         gui.CalendarButton("", target="start", image_filename="images/calendar.png", image_subsample=18)],
        [gui.In(str(event.end), key="end", size=(15, 1)),
         gui.CalendarButton("", target="end", image_filename="images/calendar.png", image_subsample=18)],
        [gui.Multiline(symps, key="symptoms", size=(15, 5))],
    ]

    layout = [
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Frame(layout=drugs, title="Drugs")],
        [gui.Submit()]
    ]

    window = gui.Window("Edit Medical Event").Layout(layout)

    button, values = window.Read()
    event.ICD10 = values["ICD10"]
    event.disease = values["disease"]
    event.response = values["response"]
    event.outcome = values["outcome"]
    if len(values["start"]) >= 10:
        event.start = date.fromisoformat(values["start"][:10])
    else:
        event.start = None
    if len(values["end"]) >= 10:
        event.end = date.fromisoformat(values["end"][:10])
    else:
        event.end = None
    event.symptoms = values["symptoms"].split("\n")
    if event.symptoms[-1] == "":
        event.symptoms.pop(-1)
    print(event.to_dict())
    #db.push_patient(patient)


# Given a patient and a hash of a Drug, creates a popup window that allows for the editing of the information in the
# Drug class
def editDrug(patient: Patient, hashcode: str = ""):
    return   # TODO


# Creates a window that asks if they're sure they want to exit without saving
# Returns true if they want to exit without saving, false otherwise
def areYouSure() -> bool:
    layout = [
        [gui.T("You are exiting an input window without saving. Are you sure you want to do this?")],
        [gui.Button("Discard the input", enable_events=True), gui.Button("Go back to editing", enable_events=True)]
    ]
    window = gui.Window("Are you sure?").Layout(layout)
    button, values = window.read()
    if button == "Discard the input":
        return True
    return False

# public static void main(String[] args){} #
if __name__ == "__main__":
    editMedicalEvent(db.get_patient(Patient(first_name="John", last_name="Doe", id_type="Driver's License",
                                            id_data="1234567890").hashcode), Medical_Event(ICD10="A37.90",
                                            disease="Whopping Cough", start=date.fromisoformat("2020-01-30")).hashcode)
