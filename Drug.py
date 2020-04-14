import datetime
import hashlib


class Drug:
    # initializer
    def __init__(self, name="", generic_name="", dosage="", side_effects=None, incompatible_drugs=None, start=None, end=None):
        self.name = name
        self.generic_name = generic_name
        self.dosage = dosage
        self.side_effects = side_effects
        self.incompatible_drugs = incompatible_drugs
        self.start = start
        self.end = end

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



if __name__ == "__main__":
    start1 = datetime.date(2000,2,29)
    end1 = datetime.date(2020,2,29)
    diseases1 = ['allergies']
    side_effects1 = ['headache','sleepiness','fatigue','nervousness','stomach pain','diarrhea','dry mouth','sore throat','hoarseness']
    drug1 = Drug('Claritin','Ioratadine','10 mg',diseases1,side_effects1,[],start1,end1)
    print(drug1)

    diseases2 = ['acne']
    side_effects2 = ['dryness','mood changes','stomach pain','nausea']
    drug2 = Drug('Accutane','Isotretinoin','1.0 mg',diseases2,side_effects2,[],start1,end1)
    print(drug2)
