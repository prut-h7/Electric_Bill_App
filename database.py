# import datetime
from kivy.storage.jsonstore import JsonStore


class DataBase:

    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.file = None
        self.prev_unit = None
        self.load()

    def load(self):
        self.file = JsonStore(self.filename)
        self.data = {}
        self.prev_unit = ""

        if self.file.exists('data1') and self.file.exists('prev'):
            mfc = self.file.get('data1')['mfc']
            ed = self.file.get('data2')['ed']
            ch1 = self.file.get('data3')['ch1']
            ch2 = self.file.get('data4')['ch2']
            ch3 = self.file.get('data5')['ch3']
            ch4 = self.file.get('data6')['ch4']
            self.prev_unit = self.file.get('prev')['valu']
            self.data['data'] = (mfc, ed, ch1, ch2, ch3, ch4)
        else:
            self.data['data']=('60', '0.15', '3.0', '4.8', '5.8', '6.2')
            self.file.put('prev', valu="0")
            self.file.put('data1', mfc="60")
            self.file.put('data2', ed="0.15")
            self.file.put('data3', ch1="3.0")
            self.file.put('data4', ch2="4.8")
            self.file.put('data5', ch3="5.8")
            self.file.put('data6', ch4="6.2")
            self.prev_unit='0'
        # self.file.close()

    def get_data(self):
        return self.data['data']

    def get_prev_data(self):
        return self.prev_unit

    def add_data(self, mfc, ed, ch1, ch2, ch3, ch4):
        self.data['data'] = (mfc.strip(), ed.strip(), ch1.strip(), ch2.strip(), ch3.strip(), ch4.strip())
        self.save_data()
        return 1

    def add_prev_data(self, prev):
        self.file.put('prev', valu=prev)

   # def validate(self, email, password):
       # if self.get_user(email) != -1:
       #     return self.users[email][0] == password
       # else:
        #    return False

    def save_data(self):
        for user in self.data:
            self.file.put('data1', mfc=self.data[user][0])
            self.file.put('data2', ed=self.data[user][1])
            self.file.put('data3', ch1=self.data[user][2])
            self.file.put('data4', ch2=self.data[user][3])
            self.file.put('data5', ch3=self.data[user][4])
            self.file.put('data6', ch4=self.data[user][5])
            #f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    #@staticmethod
    #def get_date():
        #return str(datetime.datetime.now()).split(" ")[0]