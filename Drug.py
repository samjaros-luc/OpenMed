import datetime
import hashlib


class Drug:
    # initializer
    def __init__(self, medical_event=None, name="", generic_name="", dosage="", side_effects=None, incompatible_drugs=None, start=None, end=None):
        self.medical_event = medical_event
        self.name = name
        self.generic_name = generic_name
        self.dosage = dosage
        self.side_effects = side_effects
        self.incompatible_drugs = incompatible_drugs
        self.start = start
        self.end = end
        h = hashlib.sha256()
        h.update(medical_event.hashcode.encode())
        h.update(name.encode())
        h.update(dosage.encode())
        h.update(start.encode())
        self.hashcode = h.hexdigest()

    # equals
    def __str__(self):
        string = self.name + '; ' + self.generic_name + '; ' + self.dosage + '; '
        diseases = ''
        string = string + diseases + '; '
        side_effects = ''
        for side_effect in self.side_effects:
            side_effects = side_effects + side_effect + ', '
        string = string + side_effects + '; '
        incompatible_drugs = ''
        for other_drug in self.incompatible_drugs:
            incompatible_drugs = incompatible_drugs + other_drug+', '
        string = string + incompatible_drugs + '; '
        string = string + 'Start: ' + str(self.start) + '; End: '+str(self.end)
        return string

    def to_dict(self):
        return {
            'medical_event': self.medical_event,
            'name': self.name,
            'generic_name': self.generic_name,
            'dosage': self.dosage,
            'side_effects': self.side_effects,
            'incompatible_drugs': self.incompatible_drugs,
            'start': self.start,
            'end': self.end
        }

if __name__ == "__main__":
    start1 = datetime.date(2000,2,29)
    end1 = datetime.date(2020,2,29)
    side_effects1 = ['headache','sleepiness','fatigue','nervousness','stomach pain','diarrhea','dry mouth','sore throat','hoarseness']
    drug1 = Drug('Claritin','Ioratadine','10 mg',side_effects1,[],start1,end1)
    print(drug1)

    diseases2 = ['acne']
    side_effects2 = ['dryness','mood changes','stomach pain','nausea']
    drug2 = Drug('Accutane','Isotretinoin','1.0 mg',side_effects2,[],start1,end1)
    print(drug2)
