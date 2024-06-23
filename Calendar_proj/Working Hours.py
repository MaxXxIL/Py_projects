
from Calendar_win import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import hdate
from datetime import datetime
import calendar
from pyluach import dates, hebrewcal, parshios
class my_window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_params()
        self.Init_GUI()

    def init_params(self):
        self.Month_days = {}
        self.Month_days[1]=31
        self.Month_days[2] = 28
        self.Month_days[3] = 31
        self.Month_days[4] = 30
        self.Month_days[5] = 31
        self.Month_days[6] = 30
        self.Month_days[7] = 31
        self.Month_days[8] = 31
        self.Month_days[9] = 30
        self.Month_days[10] = 31
        self.Month_days[11] = 30
        self.Month_days[12] = 31

    def Init_GUI(self):

        [yesterday,month,year,days] =self.get_data()
        indx =24
        hours_worked = 0
        hours_in_month = 0
        days_worked = 0
        days_month = 0
        for day in range(days):
            if days < indx:
                indx = 1
                month = month +1
            specific_date = datetime(year, month, indx)
            h = hdate.HDate(specific_date, hebrew=True)
            if h.dow < 5:
                if not h.is_holiday:
                    hours_in_month = hours_in_month + 9
                    if specific_date <= yesterday:
                        hours_worked = hours_worked +9
                        days_worked = days_worked +1
                days_month = days_month + 1
            elif h.dow == 5:
                if not h.is_holiday:
                    hours_in_month = hours_in_month + 8
                    if specific_date <= yesterday:
                        hours_worked = hours_worked +8
                        days_worked = days_worked + 1
                days_month = days_month + 1
            indx = indx +1
            if indx> days:
                indx =1
                month =  month+1
                if month ==13:
                    month =1
                    year=year+1
        x=1
        self.working_days.setText(str(days_month))
        self.worked_days.setText(str(days_worked))
        self.working_hours.setText(str(hours_in_month))
        self.worked_hours.setText(str(hours_worked))

    def get_data(self):
        current_date = datetime.now()
        day = current_date.day
        month = current_date.month
        year = current_date.year
        day = day -1
        if day ==0:
            day = self.Month_days(month-1)
            month=12
            year = year -1
        yesterday_time=datetime(year, month,day)

        year = current_date.year
        # check if after 23 or before - current month or previose
        if current_date.day > 23:
            month = current_date.month
        else:
            month = current_date.month - 1
            if month == 0:
                year = year - 1
                month = 12
        if month == 2:
            if calendar.isleap(current_date.year):
                days = self.Month_days[month]+1
        else:
            days = self.Month_days[month]

        return [yesterday_time,month,year,days]

    def resizeEvent(self, event):
        # This method is called when the window is resized
        print(f'Window resized: {self.size()}')


if __name__ == "__main__":
    app=QApplication(sys.argv)
    main_win=my_window()
    main_win.show()
    app.exec_()