import medical_event


class Patient:
    def __init__(self, first_name, last_name="", id_data="", id_type="", sex="N", height=-1, weight=-1):
        self.first_name = first_name
        self.last_name = last_name
        self.id_data = id_data
        self.id_type = id_type
        self.sex = sex
        self.height = height
        self.weight = weight

    def __eq__(self, other):
        if self.id_type == other.id_type and self.id_data != other.id_data:
            return False
        return self.first_name == other.first_name and self.last_name == other.last_name and self.sex == other.sex

    ## TO DO ##
    def __hash__(self):
        return 0
