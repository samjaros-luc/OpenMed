import datetime
import hashlib


class Patient:
    def __init__(self, first_name='', last_name='', dob=None, id_data='', id_type='', sex="N", height=-1, weight=-1, med_events=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.id_data = id_data
        self.id_type = id_type
        self.sex = sex
        self.height = height
        self.weight = weight
        self.med_event = med_events
        #Python's hash method using a different random seed for each run, thus
        #a different hashing method is needed
        #self.hashcode = hash((first_name+last_name+id_type+id_data))
        h = hashlib.sha256()
        h.update(first_name.encode())
        h.update(last_name.encode())
        h.update(id_type.encode())
        h.update(id_data.encode())
        self.hashcode = h.hexdigest()

    def __eq__(self, other):
        if self.id_type == other.id_type and self.id_data != other.id_data:
            return False
        return self.first_name == other.first_name and self.last_name == other.last_name and self.sex == other.sex

    def __hash__(self):
        return hash((self.first_name+self.last_name+self.id_type+self.id_data))


if __name__ == "__main__":
    #Testing Hashing
    birthday1 = datetime.date(2000,2,29)
    patient1 = Patient('Henry','Wittich',birthday1,'SSN','0000-000-000','Male',120,120,[])
    print(patient1.first_name+patient1.last_name)
    print('Hash: '+str(patient1.hashcode))

    patient2 = Patient('Henrietta','Wittich',birthday1,'SSN','0000-000-000','Male',120,120,[])
    print(patient1.first_name+patient2.last_name)
    print('Hash: '+str(patient2.hashcode))
