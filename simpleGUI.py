import PySimpleGUI as gui
from google.cloud.exceptions import Conflict
from Database import Database
from Patient import Patient
from Medical_Event import Medical_Event
from Drug import Drug
from datetime import date

gui.ChangeLookAndFeel("Purple") # TODO Customize colors
gui.SetOptions(font=("Helvetica", 12), icon="images/window_icon.ico")
idTypes = ("Driver's License", "ID Card", "Passport", "Green Card")   # Possible ID types
sexOptions = ("Female", "Male", "Unknown")   # Possible sexes
db = Database()   # Database object
windowName = "login"


# Creates & operates login window
def login() -> None:
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
        if db.userLogin(values["user"], values["pass"]):
            window.close()
            provider_menu()
            break
        else:
            gui.PopupError("Invalid username and/or password")


# After login, provides provider window which can search for a patient or create a new patient
def provider_menu() -> None:
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
            create_new_patient(first_name=values["first_name"], last_name=values["last_name"],
                               id_type=values["id_type"], id_data=values["id_data"])
            break
        elif button == "Submit":
            currentPatient = db.get_patient(Patient(first_name=values["first_name"], last_name=values["last_name"],
                                                    id_type=values["id_type"], id_data=values["id_data"]).hashcode)
            if currentPatient is None:
                window["line"].update("Patient not found. Correct information or use Create New Patient button.")
            else:
                window.close()
                display_patient(currentPatient)
                break


# Given a patient class, displays patient info, medical events, and drugs
def display_patient(patient: Patient) -> None:
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
                [gui.Button("Edit Medical Event", key="M"+event.hashcode)]
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
        elif button == "Return to Provider Menu":
            window.close()
            provider_menu()
            break
        elif button == "Edit Patient Info":
            edit_patient_info(patient)
            window.close()
            display_patient(patient)
            break
        elif button == "M":
            create_new_medical_event(patient)
            window.close()
            display_patient(patient)
            break
        elif button[0] == "M":
            hashcode = button[1:]
            edit_medical_event(patient, hashcode)
            window.close()
            display_patient(patient)
            break


# Optionally given preliminary data, pops up patient info screen and then creates new patient in database
def create_new_patient(first_name: str = "", last_name: str = "", id_type: str = "", id_data: str = "") -> None:
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
        [gui.In(first_name, key="first_name", size=(17, 1))],
        [gui.In(last_name, key="last_name", size=(15, 1))],
        [gui.InputCombo(idTypes, default_value=id_type, key="id_type", size=(15, 1))],
        [gui.In(id_data, key="id_data", size=(15, 1))],
        [gui.In(key="height", size=(15, 1))],
        [gui.In(key="weight", size=(15, 1))],
        [gui.InputCombo(sexOptions, key="sex", size=(15, 1))],
        [gui.In(str(date.today()), key="dob", size=(9, 1), pad=(2, 0)),
         gui.CalendarButton("", target="dob", image_filename="images/calendar.png", image_subsample=18)]
    ]

    layout = [
        [gui.T("Input new patient information:", key="top_text")],
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Submit(), gui.Button("Provider Menu")]
    ]

    window = gui.Window("Edit Patient Info").Layout(layout)

    while True:
        button, values = window.Read()

        if button in (None, "Quit"):
            window.close()
            break
        elif button == "Provider Menu":
            window.close()
            provider_menu()
            break
        elif button == "Submit":
            if len(values["dob"]) >= 10:
                dob = date.fromisoformat(values["dob"][:10])
            else:
                dob = None
            patient = Patient(values["first_name"], values["last_name"], dob, values["id_data"], values["id_type"],
                              values["sex"], values["height"], values["weight"])
            try:
                db.add_patient(patient)
                window.close()
                display_patient(patient)
                break
            except Conflict:
                window["top_text"].update("Patient already exists!")


# Given a patient, creates a popup window that allows for the editing of the basic information in the Patient class
def edit_patient_info(patient: Patient) -> None:
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
        [gui.In(patient.first_name, key="first_name", size=(17, 1), disabled=True)],
        [gui.In(patient.last_name, key="last_name", size=(15, 1), disabled=True)],
        [gui.InputCombo(idTypes, default_value=patient.id_type, key="id_type", size=(15, 1), disabled=True)],
        [gui.In(patient.id_data, key="id_data", size=(15, 1), disabled=True)],
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
    db.push_patient(patient)


# Given a patient, create a new medical event
def create_new_medical_event(patient: Patient) -> None:
    labels = [
        [gui.T("ICD10:")],
        [gui.T("Disease:")],
        [gui.T("Start:")],
        [gui.T("End:")],
        [gui.T("Response:")],
        [gui.T("Outcome:")],
        [gui.T("Symptoms:\nOne per line")],
    ]
    inputs = [
        [gui.In(key="ICD10", size=(15, 1))],
        [gui.In(key="disease", size=(15, 1))],
        [gui.In(str(date.today()), key="start", size=(15, 1)),
         gui.CalendarButton("", target="start", image_filename="images/calendar.png", image_subsample=20)],
        [gui.In(key="end", size=(15, 1)),
         gui.CalendarButton("", target="end", image_filename="images/calendar.png", image_subsample=20)],
        [gui.Multiline(key="symptoms", size=(15, 5))],
        [gui.In(key="response", size=(15, 1))],
        [gui.In(key="outcome", size=(15, 1))]
    ]

    layout = [
        [gui.T("ICD10, Disease, and a Start date are required.", key="top")],
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Submit()]
    ]

    window = gui.Window("Create Medical Event", resizable=True).Layout(layout)
    event = None

    while True:
        button, values = window.Read()

        if button in (None, "Quit"):
            break
        if values["ICD10"] and values["disease"] and values["start"]:
            event = Medical_Event(patient=patient.hashcode, ICD10=values["ICD10"], disease=values["disease"],
                                  start=date.fromisoformat(values["start"][:10]))
        else:
            window["top"].update("***ICD10, Disease, and a Start date are required.***")
            break
        if button == "Submit":
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
            patient.med_events.append(event)
            db.push_medical_event(event)
            db.push_patient(patient)

            window.close()
            display_patient(patient)
            break


# Given a patient and a hash of a Medical Event, creates a popup window that allows for the editing of the information
# in the Medical_Event class
def edit_medical_event(patient: Patient, hashcode: str = "") -> None:
    event = None
    for e in patient.med_events:
        if hashcode == e.hashcode:
            event = e
    if event is None:
        raise ValueError("Medical Event (hash:"+hashcode+") not found")

    drugs = [[gui.Button("Add Drug", key="D")]]
    for drug in event.drugs:
        start = [[gui.T("Start Date:")], [gui.T(str(drug.start))]]
        end = [[gui.T("End Date:")], [gui.T(str(drug.end))]]

        assembled_name = drug.name+" ("+drug.generic_name+")" if drug.name != "" and drug.generic_name != "" \
            else drug.generic_name if drug.name == "" \
            else drug.name

        side_effs = ""               # Get the side effect array as formatted string
        for se in drug.side_effects:
            side_effs = side_effs + se + ", "
        if len(side_effs) > 1:
            side_effs = side_effs[:-2]

        incompats = ""               # Get the incompatible drugs as a formatted string
        for inc in drug.incompatible_drugs:
            incompats = incompats + inc + ", "
        if len(incompats) > 1:
            incompats = incompats[:-2]

        drugs.append(
            [gui.Frame(layout=[
                [gui.T(assembled_name)],
                [gui.T(drug.dosage)],
                [gui.Column(start), gui.Column(end)],
                [gui.T("Side Effects:")],
                [gui.T(side_effs)],
                [gui.T("Incompatible Drugs:")],
                [gui.T(incompats)],
                [gui.Button("Edit This Drug", key="D"+drug.hashcode)]
            ], title="", key=drug.hashcode)]
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
        [gui.T("Symptoms:\nOne per line")],
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
        [gui.Frame(layout=drugs, title="Drugs", key="drugs_frame")],
        [gui.Submit()]
    ]

    window = gui.Window("Edit Medical Event", resizable=True).Layout(layout)

    while True:
        button, values = window.Read()

        if button in (None, "Quit"):
            break
        elif button == "D":
            create_drug(event)
            window.close()
            edit_medical_event(patient, event.hashcode)
            break
        elif button[0] == "D":
            drug_hash = button[1:]
            edit_drug(event, drug_hash)
            window.close()
            edit_medical_event(patient, hashcode)
            break
        elif button == "Submit":
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
            db.push_medical_event(event)

            window.close()
            display_patient(patient)
            break


# Given a medical event, creates a popup window that allows for the creation of a drug class
def create_drug(event: Medical_Event) -> None:
    labels = [
        [gui.T("Name:")],
        [gui.T("Generic Name:")],
        [gui.T("Dosage:")],
        [gui.T("Start:")],
        [gui.T("End:")],
        [gui.T("Side Effects:\nOne per line")],
        [gui.T("Incompatible Drugs:\nOne per line")],
    ]
    inputs = [
        [gui.In(key="name", size=(15, 1))],
        [gui.In(key="generic_name", size=(15, 1))],
        [gui.In(key="dosage", size=(15, 1))],
        [gui.In(str(date.today()), key="start", size=(15, 1)),
         gui.CalendarButton("", target="start", image_filename="images/calendar.png", image_subsample=18)],
        [gui.In(key="end", size=(15, 1)),
         gui.CalendarButton("", target="end", image_filename="images/calendar.png", image_subsample=18)],
        [gui.Multiline(key="side_effects", size=(15, 5))],
        [gui.Multiline(key="incompatible_drugs", size=(15, 5))],
    ]

    layout = [
        [gui.T("Name or Generic Name, Dosage, and Start date are required", key="top")],
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Submit()]
    ]

    window = gui.Window("Edit Drug", resizable=True).Layout(layout)
    drug = None

    while True:
        button, values = window.read()

        if button in (None, "Quit"):
            break
        if (values["name"] or values["generic_name"]) and values["dosage"] and values["start"]:
            drug = Drug(medical_event=event.hashcode, name=values["name"], generic_name=values["generic_name"],
                        dosage=values["dosage"], start=date.fromisoformat(values["start"][:10]))
        else:
            window["top"].update("***Name or Generic Name, Dosage, and Start date are required***")
        if button == "Submit":
            if len(values["end"]) >= 10:
                drug.end = date.fromisoformat(values["end"][:10])
            else:
                drug.end = None
            drug.side_effects = values["side_effects"].split("\n")
            if drug.side_effects[-1] == "":
                drug.side_effects.pop(-1)
            drug.incompatible_drugs = values["incompatible_drugs"].split("\n")
            if drug.incompatible_drugs[-1] == "":
                drug.incompatible_drugs.pop(-1)
            event.drugs.append(drug)
            db.push_medical_event(event)
            db.push_drug(drug)

            window.close()


# Given a patient and a hash of a Drug, creates a popup window that allows for the editing of the information in the
# Drug class
def edit_drug(event: Medical_Event, hashcode: str = "") -> None:
    drug = None
    for d in event.drugs:
        if d.hashcode == hashcode:
            drug = d
    if drug is None:
        raise ValueError("Drug (hash:"+hashcode+") could not be found")

    side_effs = ""               # Get the side effect array as formatted string
    for se in drug.side_effects:
        side_effs = side_effs + se + "\n"
    if len(side_effs):
        side_effs = side_effs[:-1]

    incompats = ""               # Get the incompatible drugs as a formatted string
    for inc in drug.incompatible_drugs:
        incompats = incompats + inc + "\n"
    if len(incompats):
        incompats = incompats[:-1]

    labels = [
        [gui.T("Name:")],
        [gui.T("Generic Name:")],
        [gui.T("Dosage:")],
        [gui.T("Start:")],
        [gui.T("End:")],
        [gui.T("Side Effects:\nOne per line")],
        [gui.T("Incompatible Drugs:\nOne per line")],
    ]
    inputs = [
        [gui.In(drug.name, key="name", size=(15, 1))],
        [gui.In(drug.generic_name, key="generic_name", size=(15, 1))],
        [gui.In(drug.dosage, key="dosage", size=(15, 1))],
        [gui.In(str(drug.start), key="start", size=(15, 1)),
         gui.CalendarButton("", target="start", image_filename="images/calendar.png", image_subsample=18)],
        [gui.In(str(drug.end), key="end", size=(15, 1)),
         gui.CalendarButton("", target="end", image_filename="images/calendar.png", image_subsample=18)],
        [gui.Multiline(side_effs, key="side_effects", size=(15, 5))],
        [gui.Multiline(incompats, key="incompatible_drugs", size=(15, 5))],
    ]

    layout = [
        [gui.Column(labels), gui.Column(inputs)],
        [gui.Submit()]
    ]

    window = gui.Window("Edit Drug", resizable=True).Layout(layout)

    button, values = window.read()

    if button == "Submit":
        drug.name = values["name"]
        drug.generic_name = values["generic_name"]
        drug.dosage = values["dosage"]
        if len(values["start"]) >= 10:
            drug.start = date.fromisoformat(values["start"][:10])
        else:
            drug.start = None
        if len(values["end"]) >= 10:
            drug.end = date.fromisoformat(values["end"][:10])
        else:
            drug.end = None
        drug.side_effects = values["side_effects"].split("\n")
        if drug.side_effects[-1] == "":
            drug.side_effects.pop(-1)
        drug.incompatible_drugs = values["incompatible_drugs"].split("\n")
        if drug.incompatible_drugs[-1] == "":
            drug.incompatible_drugs.pop(-1)
        db.push_drug(drug)

        window.close()


# ### Currently Unused ###
# Creates a window that asks if they're sure they want to exit without saving
# Returns true if they want to exit without saving, false otherwise
def are_you_sure() -> bool:
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
    login()
