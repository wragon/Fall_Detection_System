# About User Info

class UserInfo:
    name = ""
    number = ""
    location = "" 

    def __init__(self):
        self.set_user()

    def set_user(self):
        self.set_name()
        self.set_number()
        self.set_location()

    def set_name(self):
        self.name = input ("사용자 이름: ")
        #self.name = "" # todo yourself

    def set_number(self):
        self.number = input ("보호자 연락처: ")
        #self.number = "" # todo yourself

    def set_location(self):
        self.location = input ("사용자 위치: ")
        #self.location = "" # todo yourself

    def get_user(self):
        print(self.name)
        print(self.number)
        print(self.location)

    def get_name(self):
        return self.name

    def get_number(self):
        return self.number

    def get_location(self):
        return self.location

