import datetime

class Drug:
    #initializer
    def __init__(self, name="", generic_name="",dosage="",diseases=[],side_effects=[],incompatible_drugs=[]):
        self.name = name
        self.generic_name = generic_name
        #Currently using dosage as a string so that we can include units.
        #Is it beneficial to make dosage a numerical value?
        self.dosage = dosage
        self.diseases = diseases
        self.side_effects = side_effects
        self.incompatible_drugs = incompatible_drugs
        #We previously talked about including a start and end date for a drug,
        #do we feel this is covered in the Medical_Event class?

    #accessors
    def get_name(self):
        return self.name

    def get_generic_name(self):
        return self.generic_name

    def get_dosage(self):
        return self.dosage

    def get_diseases(self):
        return self.diseases

    def get_side_effects(self):
        return self.side_effects

    #mutators

    #equals
    def __eq__(self,other):
