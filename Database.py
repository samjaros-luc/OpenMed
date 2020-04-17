import firebase_admin
from firebase_admin import credentials, firestore
from firebase import Firebase as fb
# For interacting with companion classes
from Patient import Patient
from Medical_Event import Medical_Event
from Drug import Drug
from datetime import date

class Database:
    config = None   # firebase config

    p = None   # Patient collection reference
    m = None   # Medical event collection reference
    drug = None   # Drugs collection reference
    user = None   # User reference
    token = ""   # User's token to use when getting/pushing

    def __init__(self):
        # Access collections via service account
        # Get credentials using token from service account (.json file, Sam can send it to you)
        cred = credentials.Certificate("C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/openmed-comp363-firebase-adminsdk-qglti-767b82d10f.json")
        # Create instance of application
        app = firebase_admin.initialize_app(cred)

        client = firestore.client(app)   # Create handle
        self.p = client.collection("patients")   # Patient collection
        self.m = client.collection("medical_events")   # Medical event collection
        self.d = client.collection("drugs")   # Drugs collection

    def userLogin(self, username, password):
        config = {
            "apiKey": "AIzaSyDuEowvI82yDtNdQIdYzL_4xKdCz6iFuHo",
            "authDomain": "openmed-comp363.firebaseapp.com",
            "databaseURL": "https://openmed-comp363.firebaseio.com",
            "storageBucket": "openmed-comp363.appspot.com",
            "serviceAccount": "openmed-comp363-firebase-adminsdk-qglti-767b82d10f.json"
        }

        client = fb(config)
        auth = client.auth()

        try:
            self.user = auth.sign_in_with_email_and_password(username, password)
            return True
        except: return False

    # Given patient info, it grabs the patient record
    # Required input: dictionary with "first_name", "last_name", "id_type", and "id_data" defined
    def get_patient(self, hashcode):
        pat = self.p.document(hashcode).get()
        pat_data = pat.to_dict()
        if pat.exists:
            med_events = []
            for event in pat_data["med_events"]:
                me_doc = self.m.document(event).get()
                me_doc_data = me_doc.to_dict()
                drugs = []
                for drug in me_doc_data["drugs"]:
                    drug_doc = self.d.document(drug).get()
                    drug_doc_data = drug_doc.to_dict()
                    drugs.append(Drug(name=drug_doc_data["name"], generic_name=drug_doc_data["generic_name"],
                                      dosage=drug_doc_data["dosage"], side_effects=drug_doc_data["side_effects"],
                                      start=drug_doc_data["start"], end=drug_doc_data["end"]))
                med_events.append(Medical_Event(ICD10=me_doc_data["ICD10"], disease=me_doc_data["disease"], start=me_doc_data["start"],
                                                end=me_doc_data["end"], drugs=drugs, outcome=me_doc_data["outcome"], response=me_doc_data["response"]))
            return Patient(first_name=pat_data["first_name"], last_name=pat_data["last_name"],
                           id_type=pat_data["id_type"], id_data=pat_data["id_data"], dob=pat_data["dob"],
                           sex=pat_data["sex"], height=pat_data["height"], weight=pat_data["weight"],
                           med_events=med_events)
        else:
            return None

    # Given a patient and the fields that need to be updated, update them
    def push_patient(self, patient):
        pat = self.p.document(patient.hashcode)
        pat.update(patient.to_dict())

    # Given a medical event and the fields that need to be updated, update them
    def push_medical_event(self, medical_event):
        me = self.m.document(medical_event.hashcode)
        me.update(medical_event.to_dict())

    def push_drug(self, drug):
        dr = self.d.document(drug.hash)
        dr.update(drug.to_dict())

if __name__ == "__main__":
    foo = Database()
    try:
        foo.userLogin(username="wrong",password="wrong")
    except:
        print("Sign-in correctly failed")

    foo.userLogin(username="pass_is_password@gmail.com", password="password")
    print("Sign-in correctly succeeded")

    pat = db.get_patient(Patient(first_name="John", last_name="Doe", id_type="Driver's License", id_data="1234567890").hashcode)
    print("Patient received:\n"+str(pat.to_dict()))



