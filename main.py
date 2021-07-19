from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase


class CreateAccountWindow(Screen):
    mfc = ObjectProperty(None)
    ed = ObjectProperty(None)
    ch1 = ObjectProperty(None)
    ch2 = ObjectProperty(None)
    ch3 = ObjectProperty(None)
    ch4 = ObjectProperty(None)

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def submit(self):

        if self.mfc.text.isnumeric():
            if self.isfloat(self.ed.text) and self.isfloat(self.ch1.text) and self.isfloat(self.ch2.text) and self.isfloat(self.ch3.text) and self.isfloat(self.ch4.text):
              db.add_data(self.mfc.text, self.ed.text, self.ch1.text, self.ch2.text, self.ch3.text, self.ch4.text)
              sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"


    def reset(self):
        mfc, ed, ch1, ch2, ch3, ch4 = db.get_data()
        self.mfc.text = mfc
        self.ed.text = ed
        self.ch1.text = ch1
        self.ch2.text = ch2
        self.ch3.text = ch3
        self.ch4.text = ch4

    def data1(self):
        self.reset()
        return self.mfc.text

    def data2(self):
        return self.ed.text

    def data3(self):
        return self.ch1.text

    def data4(self):
        return self.ch2.text

    def data5(self):
        return self.ch3.text

    def data6(self):
        return self.ch4.text

class LoginWindow(Screen):

    this_month = ObjectProperty(None)
    prev_month = ObjectProperty(None)
    bill = ObjectProperty(None)

    def pre_month(self):
        self.prev_month.text = db.get_prev_data()
        return self.prev_month.text

    def loginBtn(self):
        #self.prev_month.text=db.get_prev_data()

        if (self.this_month.text.isnumeric() == True) and (self.prev_month.text.isnumeric() == True) and (int(self.this_month.text) > int(self.prev_month.text)) :
            self.calculate()
            MainWindow.curr_bill = str(self.bill)
            MainWindow.curr_unit=str(int(self.this_month.text)-int(self.prev_month.text))
            db.add_prev_data(self.this_month.text)
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def calculate(self):
        mfc, ed, ch1, ch2, ch3, ch4 = db.get_data()
        prev_month = int(self.prev_month.text)
        this_month = int(self.this_month.text)
        z = this_month-prev_month

        if z < 50:
            self.bill = (z * float(ch1)) + float(mfc) + (float(ed) * z)
        elif 50 < z < 200:
            k = z - 50
            self.bill = (50 * float(ch1)) + (k * float(ch2)) + float(mfc) + (float(ed) * z)
        elif 200 < z < 400:
            k = z - 200
            self.bill = (50 * float(ch1)) + (150 * float(ch2)) + (k * float(ch3)) + float(mfc) + (float(ed) * z)
        else:
            k = z - 400
            self.bill = (50 * float(ch1)) + (150 * float(ch2)) + (200 * float(ch3)) + (k * float(ch4)) + float(mfc) + (float(ed) * z)

    def createBtn(self):
        #self.reset()
        sm.current = "create"

    def reset(self):
        self.prev_month.text = self.this_month.text
        self.this_month.text = ""



class MainWindow(Screen):
    bill=ObjectProperty(None)
    unit=ObjectProperty(None)
    curr_bill = ""
    curr_unit = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, **args):
        self.bill.text = "Total Bill: Rs. " + self.curr_bill
        self.unit.text = "Total Units: " + self.curr_unit
        # self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Input',
                  content=Label(text='Invalid input.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Input',
                  content=Label(text='Fill inputs with valid information.'),
                  size_hint=(None, None), size=(500, 500))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("data.json")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()