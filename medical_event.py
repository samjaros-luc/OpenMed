import datetime
import Drug
import disease

class Medical_Event:

    def __init__(self, title="", symptoms=[], start="", end="", response="", outcome=""):
        self.title = title
        self.symptoms = symptoms
        self.start = start
        self.end = end
        self.response = response
        self.outcome = outcome

    def get_title(self):
        return self.title

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

    def update_outcome(self, end, response, outcome):
        self.end = end
        self.response = response
        self.outcome = outcome

    def print_info(self):
        print("Event: " + self.title + "; Start Date: " + self.start + "; End Date: " + self.end)
        symptoms = ""
        for symptom in self.symptoms:
            symptoms = symptoms + symptom + ", "
        print("Symptoms: " + symptoms)
        print("Response: " + self.response)
        print("Outcome: " + self.outcome)



#Test:

symptoms1 = ["coughing", "runny nose", "sneezing"]
med_event1 = Medical_Event("common cold", symptoms1, "1/1/20", "1/5/20", "Given tylenol.", "Cold went away.")
print(med_event1.get_symptoms())
print(med_event1.get_start())

symptoms2 = ["coughing", "weezing", "shortness of breath"]
med_event2 = Medical_Event("asthma", symptoms2, "1/1/20", None, "Given inhaler.", "Condition managed.")
print(med_event2.get_end())
print(med_event2.get_response())
print(med_event2.get_outcome())


symptoms3 = ["coughing", "weezing", "shortness of breath"]
med_event3 = Medical_Event("asthma attack", symptoms3, "2/1/20", "2/2/20", "Given inhaler.", "Stopped asthma attack.")
print(med_event3.get_end())
print(med_event3.get_response())
print(med_event3.get_outcome())
med_event3.print_info()

#Cure for asthma is created:

med_event2.update_outcome("3/6/20", "Given cure.", "Asthma cured.")
print(med_event2.get_end())
print(med_event2.get_response())
print(med_event2.get_outcome())
med_event2.print_info()












