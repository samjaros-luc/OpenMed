import datetime
import hashlib


class Medical_Event:

    def __init__(self, patient=None, ICD10="", disease="", drugs=[], symptoms=[], start=None, end=None, response="", outcome=""):
        self.patient = patient
        self.ICD10 = ICD10_code
        self.disease = disease
        self.drugs = drugs
        self.symptoms = symptoms
        self.start = start
        self.end = end
        self.response = response
        self.outcome = outcome
        h = hashlib.sha256()
        h.update(patient.hashcode.encode())
        h.update(ICD10_code.encode())
        h.update(disease.encode())
        h.update(start.encode())
        self.hashcode = h.hexdigest()

    def __str__(self):
        string = self.ICD10 + "; " + self.disease + "; " + str(self.start) + "; " + str(self.end) + "; "
        symptoms = ""
        for symptom in self.symptoms:
            symptoms = symptoms + symptom + ", "
        string = string + symptoms
        drugs = ""
        for drug in self.drugs:
            drugs = drugs + drug + ", "
        string = string + "; " + drugs + "; " + self.response + "; " + self.outcome
        return string

    def update_outcome(self, end, drugs, response, outcome):
        self.end = end
        self.drugs = drugs
        self.response = response
        self.outcome = outcome

    def print_info(self):
        print("Event code: " + self.ICD10 + "; " + self.disease + "; Start Date: " + str(self.start) + "; End Date: " + str(self.end))
        symptoms = ""
        for symptom in self.symptoms:
            symptoms = symptoms + symptom + ", "
        drugs = ""
        for drug in self.drugs:
            drugs = drugs + drug + ", "
        print("Drug(s) Prescribed: " + drugs)
        print("Symptoms: " + symptoms)
        print("Response: " + self.response)
        print("Outcome: " + self.outcome)

    def to_dict(self):
        drug_list = []
        for drug in self.drugs:
            drug_list.append(drug.hexcode)
        return {
            'patient_hash': self.patient.hashcode,
            'ICD10': self.ICD10,
            'disease': self.disease,
            'drugs': drug_list,
            'start': self.start,
            'end': self.end,
            'response': self.response,
            'outcome': self.outcome,
            'symptoms': self.symptoms
        }


if __name__ == "__main__":
    start1 = datetime.date(2020, 1, 1)
    end1 = datetime.date(2020, 1, 5)
    symptoms1 = ["coughing", "runny nose", "sneezing"]
    med_event1 = Medical_Event("N/A", "common cold", [], symptoms1, start1, end1, "Given tylenol.", "Cold went away.")
    print(med_event1.get_symptoms())
    print(med_event1.get_start())

    start2 = datetime.date(2020, 1, 1)
    symptoms2 = ["coughing", "weezing", "shortness of breath"]
    med_event2 = Medical_Event("N/A", "asthma", [], symptoms2, start2, None, "Given inhaler.", "Condition managed.")
    print(med_event2.get_end())
    print(med_event2.get_response())
    print(med_event2.get_outcome())

    start3 = datetime.date(2020, 2, 1)
    end3 = datetime.date(2020, 2, 2)
    symptoms3 = ["coughing", "weezing", "shortness of breath"]
    med_event3 = Medical_Event("N/A", "asthma attack", [], symptoms3, start3, end3, "Given inhaler.", "Stopped asthma attack.")
    print(med_event3.get_end())
    print(med_event3.get_response())
    print(med_event3.get_outcome())
    med_event3.print_info()

    #Cure for asthma is created:

    end2 = datetime.date(2020, 3, 6)
    drug = ["cure"]
    med_event2.update_outcome(end2, drug,  "Given cure.", "Asthma cured.")
    print(med_event2.get_end())
    print(med_event2.get_response())
    print(med_event2.get_outcome())
    med_event2.print_info()
