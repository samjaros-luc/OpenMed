#import drug
import disease
import datetime

class Medical_Event:

    def __init__(self, ICD10_code="", disease=None, drugs=[], symptoms=[], start=None, end=None, response="", outcome=""):
        self.ICD10_code = ICD10_code
        self.disease = disease
        self.drugs = drugs
        self.symptoms = symptoms
        self.start = start
        self.end = end
        self.response = response
        self.outcome = outcome

    def __str__(self):
        string = self.ICD10_code + "; " + self.disease + "; " + str(self.start) + "; " + str(self.end) + "; "
        symptoms = ""
        for symptom in self.symptoms:
            symptoms = symptoms + symptom + ", "
        string = string + symptoms
        drugs = ""
        for drug in self.drugs:
            drugs = drugs + drug + ", "
        string = string + "; " + drugs + "; " + self.response + "; " + self.outcome
        return string

    def get_ICD10_code(self):
        return self.ICD10_code

    def get_symptoms(self):
        return self.symptoms
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_response(self):
        return self.response

    def get_outcome(self):
        return self.outcome

    def update_outcome(self, end, drugs, response, outcome):
        self.end = end
        self.drugs = drugs
        self.response = response
        self.outcome = outcome

    def print_info(self):
        print("Event code: " + self.ICD10_code + "; " + self.disease + "; Start Date: " + str(self.start) + "; End Date: " + str(self.end))
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



#Test:

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


print(str(med_event2))












