# For interacting with firebase
import firebase_admin
from firebase_admin import credentials, auth, firestore
# For interacting with companion classes
from Patient import Patient
from Medical_Event import Medical_Event
from Drug import Drug
import datetime



class Database:
    p = None   # Patient collection reference
    m = None   # Medical event collection reference
    drug = None   # Drugs collection reference

    def __init__(self, username, password):
        # TODO get token for user to create handle

        ### TEMPORARY access collections via service account
        # Get creditentails using token from service account (.json file, Sam can send it to you)
        cred = credentials.Certificate("C:/Users/samja/OneDrive/Loyola - Semester 8/COMP 363/OpenMed/openmed-comp363-firebase-adminsdk-qglti-767b82d10f.json")
        # Create instance of application
        app = firebase_admin.initialize_app(cred)

        client = firestore.client(app)   # Create handle
        self.p = client.collection("patients")   # Patient collection
        self.m = client.collection("medical_events")   # Medical event collection
        self.d = client.collection("drugs")   # Drugs collection

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
                    drug_doc = self.d.document(drug)
                    drug_doc_data = drug_doc.to_dict()
                    drugs.append(Drug(name=drug_doc_data["name"], generic_name=drug_doc_data["generic_name"],
                                      dosage=drug_doc_data["dosage"], side_effects=drug_doc_data["side_effects"],
                                      start=drug_doc_data["start"], end=drug_doc_data["data"]))
                med_events.append(Medical_Event(ICD10_code=me_doc_data["ICD10"], disease=me_doc_data["disease"], start=me_doc_data["start"],
                                                end=me_doc_data["end"], drugs=drugs, outcome=me_doc_data["outcome"], response=me_doc_data["response"]))
            return Patient(first_name=pat_data["first_name"], last_name=pat_data["last_name"],
                           id_type=pat_data["id_type"], id_data=pat_data["id_data"], dob=pat_data["dob"],
                           sex=pat_data["sex"], height=pat_data["height"], weight=pat_data["weight"],
                           med_events=med_events)
        else:
            return None

    # Given a hash for a patient and dictionaries of class attributes to be updated, this method updates patient info
    def updatePatient(self, hashcode, updated_fields):
        pat = self.get_patient(hashcode)
        p_keys = list(p_dic.keys)       
        for key in p_keys:
            p_doc.data[key] = p_dic.get(key)                
        print("Patient data updated.")
        return

    #need ref to medical event and dic with attributes to update
    def updateMedicalEvent(self, ref, m_dic):
        m_keys = list(m_dic.keys)
        m_doc = self.m.document(ref)
            for key in m_keys:
                m_doc.data[key] = m_dic.get(key)
        return

    def newMedicalEvent(self, hashcode, m_dic):
        p_doc = getPatient(self, hashcode)
        #generate ref for med event in some way..
        ref = ""
        p_doc.data["med_events"].append(ref)
        #make new document in medical_events collection
        m_doc = self.m.document(
            #reference
            )
        m_keys = list(m_dic.keys)
        for key in m_keys:
            m_doc.data[key] = m_dic.get(key)
        return

    def updateDrug(self, ref, drug_dic):
        drug_keys = list(drug_dic.keys)
        drug_doc = self.drug.document(ref)
            for key in drug_keys:
                drug_doc.data[key] = drug_dic.get(key)
        return
        
    #need me_ref to know which med event to update
    def newDrug(self, me_ref, drug_dic):
        m_doc = self.m.document(me_ref)
        #generate ref for drug in some way..
        ref = ""
        m_doc.data["drugs"].append(ref)
        #make new document in medical_events collection
        drug_doc = self.drug.document(
            #reference
            )
        drug_keys = list(drug_dic.keys)
        for key in drug_keys:
            drug_doc.data[key] = drug_dic.get(key)
        return

    # Given a new patient, it will add it to the database
    def newPatient(self, patient):
        # TODO
        hashcode = patient.hashcode
        #make new document in patients collection
        p_doc = self.p.document(hashcode)
        #make new data entries for document
        p_doc.data["first_name"] = patient.first_name
        last_name = patient.last_name
        p_doc.data["last_name"] = last_name 
        dob = patient.dob
        p_doc.data["dob"] = dob 
        id_data = id_data
        p_doc.data["id_data"] = id_data 
        id_type = patient.id_type
        p_doc.data["id_type"] = id_type
        sex = patient.sex
        p_doc.data["sex"] = sex 
        height = patient.height
        p_doc.data["height"] = height 
        weight = patient.weight
        p_doc.data["weight"] = weight
        #should be a list of references...
        med_events = patient.med_events
        p_doc.data["med_events"] = med_events
        
        for med_event in med_events:
            #make new document in medical_events collection
            m_doc = self.m.document(
                #reference
                )
            #make new data entries for document
            ICD10_code = med_event.ICD10_code
            m_doc.data["ICD10_code"] = ICD10_code
            disease = med_event.disease
            m_doc.data["disease"] = disease
            #should be a list of references
            drugs = med_event.drugs
            m_doc.data["drugs"] = drugs
            symptoms = med_event.symptoms
            m_doc.data["symptoms"] = symptoms
            start = med_event.start
            m_doc.data["start"] = start
            end = med_event.end
            m_doc.data["end"] = end
            response = med_event.response
            m_doc.data["response"] = response
            outcome = med_event.outcome
            m_doc.data["outcome"] = outcome 

            for drug in drugs:
                #make new documnet in drugs collection
                drug_doc = self.drug.document(
                    #reference
                    )
                #make new data entries for document
                name = drug.name
                drug_doc.data["name"] = name
                generic_name = drug.generic_name
                drug_doc.data["generic_name"] = generic_name
                dosage = drug.dosage
                drug_doc.data["dosage"] = dosage
                diseases = drug.diseases
                drug_doc.data["diseases"] = diseases
                side_effects = drug.side_effects
                drug_doc.data["side_effects"] = side_effects
                incompatible_drugs = drug.incompatible_drugs
                drug_doc.data["incompatible_drugs"] = incompatible_drugs
                start = drug.start
                drug_doc.data["start"] = start
                end = drug.end
                drug_doc.data["end"] = end

        print("New patient added to database.")
        return


if __name__ == "__main__":
    Database(username="admin", password="admin")
    # TODO class testing
   
