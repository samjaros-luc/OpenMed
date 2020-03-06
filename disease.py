class Disease:
    def __init__(self, name="", symptoms=[], start="", end=""):
        self.name = name
        self.symptoms = symptoms
        self.start = start
        self.end = end

    def __eq__(self, other):
        if self.id_type == other.id_type and self.id_data != other.id_data:
            return False
        return self.first_name == other.first_name and self.last_name == other.last_name and self.sex == other.sex


    def get_symptoms(self):
        return self.symptoms


#Test:

symptoms = ["cough", "runny nose", "sneeze"]
disease1 = Disease("common cold", symptoms, "1/1/20", "1/5/20")

print(disease1.symptoms)

print(disease1.get_symptoms())
