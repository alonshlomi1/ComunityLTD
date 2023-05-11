import uuid

class Client:
    def __init__(self, first_name, last_name, phone, email, id= None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def __str__(self):
        return "\n" + self.id + "\n" + self.first_name +" "+ self.last_name +"\t"+ self.phone +"\t"+ self.email
    def __repr__(self):
        return self.__str__()