from google.cloud import firestore
from Patient import Patient
from Medical_Event import Medical_Event
from Drug import Drug
from Disease import Disease
import datetime


class Database:
    client = firestore.Client()
    p = client.collection(u'patients')   # Patient collection
    m = client.collection(u'medical_events')   # Medical event collection
    dis = client.collection(u'diseases')   # Diseases collection
    drug = client.collection(u'drugs')   # Drugs collection

    # Given patient info, it grabs the patient record
    # Required input: dictionary with "first_name", "last_name", "id_type", and "id_data" defined
    def getPatient(self, dict={}, hash=""):
        if hash == "":
            doc = self.p.document(Patient(first_name=dict["first_name"], last_name=dict["last_name"],
                                          id_type=dict["id_type"], id_data=dict["id_data"]).hashcode)
        else:
            doc = self.p.document(hash)
        if doc.exists:
            med_events = []
            for event in doc.data["med_events"]:
                me_doc = self.m.document(event)
                drugs = []
                for drug in me_doc.data["drugs"]:
                    drug_doc = self.drug.document(drug)
                    drugs.append(Drug(name=drug_doc.data["name"], generic_name=drug_doc.data["generic_name"],
                                      dosage=drug_doc.data["dosage"], side_effects=drug_doc.data["side_effects"],
                                      start=drug_doc.data["start"], end=drug_doc.data["data"]))
                dis_doc = self.dis.document(me_doc.data["disease"])
                disease = (Disease(name=dis_doc.data["name"], symptoms=dis_doc.data["symptoms"],
                                   start=dis_doc.data["start"], end=dis_doc.data["end"]))
                med_events.append(Medical_Event(ICD10_code=me_doc.data["ICD10"], start=me_doc.data["start"],
                                                end=me_doc.data["end"], disease=disease, drugs=drugs,
                                                outcome=me_doc.data["outcome"], response=me_doc.data["response"]))
            return Patient(first_name=doc.data["first_name"], last_name=doc.data["last_name"],
                           id_type=doc.data["id_type"], id_data=doc.data["id_data"], dob=doc.data["dob"],
                           sex=doc.data["sex"], height=doc.data["height"], weight=doc.data["weight"],
                           med_events=med_events)
        # elif the patient doesn't exist
        return None

    # Given a hash and a dictionary of values to update, it gets the patient record and changes it
    def updatePatient(self, hash, dict):
        # TODO
        return Patient()

    # Given a new patient, it will add it to the database
    def newPatient(self, patient):
        # TODO
        return Patient()
