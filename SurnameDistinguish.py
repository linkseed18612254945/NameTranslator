import os

BASE_DIR = os.path.dirname(__file__)
PATH = BASE_DIR+'/Double_Surname.dict'
with open(PATH, 'r') as f:
    raw = f.read()
    DOUBLE_NAME = raw.split('、')


class NameDistinguish:
    def __init__(self, ch_name):
        self.ch_name = ch_name
        self.surname = ''
        self.first_name = ''

    def get_names(self):
        if len(self.ch_name) == 2:
            self.surname = self.ch_name[0]
            self.first_name = self.ch_name[1]
        else:
            if self.double_search():
                self.surname = self.ch_name[:2]
                self.first_name = self.ch_name[2:]
            else:
                self.surname = self.ch_name[:1]
                self.first_name = self.ch_name[1:]
        return [self.surname, self.first_name]

    def double_search(self):
        for i in DOUBLE_NAME:
            if self.ch_name[:2] == i:
                return True
        return False

