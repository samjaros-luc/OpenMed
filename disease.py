class Disease:
    def __init__(self, name="", symptoms=[], start="", end=""):
        self.name = name
        self.symptoms = symptoms
        self.start = start
        self.end = end

    def get_symptoms(self):
        return self.symptoms

#Test:

symptoms = ["cough", "runny nose", "sneeze"]
disease1 = Disease("common cold", symptoms, "1/1/20", "1/5/20")

print(disease1.symptoms)
print(disease1.get_symptoms())
