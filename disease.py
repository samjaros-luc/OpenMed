import datetime

class Disease:
    def __init__(self, name="", symptoms=[], start="", end=""):
        self.name = name
        self.symptoms = symptoms
        self.start = start
        self.end = end

    def __str__(self):
        string = self.name + "; "
        symptoms = ""
        for symptom in self.symptoms:
            symptoms = symptoms + symptom + ", "
        string = string + symptoms + "; " + str(self.start) + "; " + str(self.end)
        return string
        
    def get_symptoms(self):
        return self.symptoms


#Test:

symptoms = ["cough", "runny nose", "sneeze"]
start = datetime.date(2020, 1, 1)
end = datetime.date(2020, 1, 5)
disease1 = Disease("common cold", symptoms, start, end)

print(disease1.symptoms)

print(disease1.get_symptoms())

print(str(disease1))
