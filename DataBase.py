import pymssql
import SurnameDistinguish
import re
import pypinyin
from pypinyin import pinyin

HOST = 'localhost'
USER = 'sa'
PASSWORD = '123'
DATABASE = 'tr'


class DataBaseConnector:
    def __init__(self, ch_name):
        self.conn = pymssql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        self.cursor = self.conn.cursor()
        self.ch_name = ch_name
        self.names = SurnameDistinguish.NameDistinguish(self.ch_name).get_names()
        self.en_name_list = []
        self.best = ''

    def search(self):
        self.cursor.execute("""
        SELECT [en_name],[frequence] FROM zzname WHERE ch_name=%s""", self.ch_name)
        row = self.cursor.fetchall()
        if not row:
            self.best = self.get_pinyin()[0].title()
            return [['', '']]
        row.sort(key=lambda x: x[1])
        for i in row:
            self.en_name_list.append(i[0])
        source_name = []
        row.reverse()
        for i in row:
            source_name.append(i[0])
        self.best = self.adjust(source_name)
        self.conn.commit()
        row.reverse()
        return row

    def adjust(self, source_name):
        pattern = r'[ -.]'
        py = self.get_pinyin()
        for i in source_name:
            letters = i.lower()
            en_names = re.split(pattern, letters)
            forward_name = ' '.join(en_names)
            en_names.reverse()
            reverse_name = ' '.join(en_names)
            en_names.reverse()
            for j in py:
                if forward_name == j or reverse_name == j:
                    return j.title()

    def get_pinyin(self):
        su_temp = pinyin(self.names[0], style=pypinyin.NORMAL,heteronym=True)
        fn_temp = pinyin(self.names[1], style=pypinyin.NORMAL, heteronym=True)
        su_py = self.combination(self, su_temp, '')
        fn_py = self.combination(self, fn_temp, '')
        pys = self.combination(self, [su_py, fn_py], ' ')
        return pys

    @staticmethod
    def combination(self, tokens, connector):
        len_name = len(tokens)
        comb = []
        if len_name == 1:
            comb = tokens[0]
        if len_name == 2:
            for i in tokens[0]:
                for j in tokens[1]:
                    comb.append(connector.join([i, j]))
        if len_name == 3:
            for i in tokens[0]:
                for j in tokens[1]:
                    for k in tokens[2]:
                        comb.append(connector.join([i, j, k]))
        return comb

    def close(self):
        self.conn.close()


def init_connect():
    DataBaseConnector('')
