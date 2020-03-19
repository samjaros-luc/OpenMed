import datetime
from datetime import date

class Disease:
    def __init__(self, name, start, end=None, symptoms=[]):
        self.name = name
        self.symptoms = symptoms
        self.start = start
        self.end = end
        self.symptoms = symptoms

    def unpack(self, unpack):
        args = unpack.split(";")
        name = args[0]
        args[1] = args[1][2:-2]
        symptoms = args[1].split("', '")
        start = date.fromisoformat(args[2])
        end = date.fromisoformat(args[3])
        return Disease(name, start, end, symptoms)

    def __str__(self):
        return self.name + ";" + str(self.symptoms) + ";" + str(self.start) + ";" + str(self.end)

    def get_symptoms(self):
        return self.symptoms

#Test:

symptoms = ["cough", "runny nose", "sneeze"]
start = datetime.date(2020, 1, 1)
end = datetime.date(2020, 1, 5)
disease1 = Disease("common cold", start, end, symptoms)

print(disease1.symptoms)
print(disease1.get_symptoms())
print(str(disease1))
disease2 = Disease.unpack(str(disease1))
print(str(disease2))