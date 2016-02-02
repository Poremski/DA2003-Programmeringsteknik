# -*- coding: UTF-8 -*-
from time import localtime

# Titel: 110 Kalender
# Författare: Andreas Poremski
# Datum: 2016-02-02
#
# Program som skriver ut en kalender för ett godtyckligt år i intervallet 1900 och 3000.

class Date:
    """ Klassen 'Date' håller koll på kalendermånaden för vald år och månad.
    """
    def __init__(self, year, month):
        """ Konstruktorn för klassen 'Date'.
    
        Argument:
            year  (int): heltal motsvarande årtalet mellan intervallet 1900-3000.
            month (int): heltal motsvarande månaden mellan intervallet 1-12 (jan-dec).
        """
        self.MIN_YEAR = 1900
        self.MAX_YEAR = 3000
        self.year = year
        self.month = month
    
    def isLeapYear(self, year):
        """ Kontroll om året är skottår eller ej.
        
        Returnerar:
            (boolean): 'True' om året är skottår, annars 'False'.
        """
        return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        
    def getLastDayOfMonth(self, month):
        """ Returnerar månadens sista dag.
        
        Returnerar:
            (int): ett heltal mellan 28 och 31.
        
        """
        days_each_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # 0-11 (jan-dec)
        if not self.isLeapYear(self.year) or month != 2 and self.isLeapYear(self.year):
            return days_each_month[month-1]
        else:
            return 29
        
    def getDayOfTheWeek(self, day):
        """ Ger veckodagen för det angivna datumet.
        
        Argument:
            day (int): heltal motsvarande kalenderdagen mellan intervallet 1-31.
        
        Returnerar:
            (int): siffra mellan 0 och 6 där 1 motsvaras av måndag och 7 av söndag.
        """
        return (self.getDurationDays(self.month, day)) % 7
    
    def getDurationDays(self, month, day):
        """ Ger antalet dagar sedan 1900-01-01 fram till given månad och dag; det givna dagen inkluderas ej.
        
        Argument:
            month (int): heltal motsvarande månaden mellan intervallet 1-12 (jan-dec).
            day (int): heltal motsvarande kalenderdagen mellan intervallet 1-31.
            
        Returnerar:
            (int): antalet dagar sedan 1900-01-01; innevarande dag ej medräknad.
        """
        # År till dagar
        sum_days = (self.year - self.MIN_YEAR)*365 + self.getLeapDays()
        # Månader till dagar
        if month >= 2:
            for i in range(1, month):
                sum_days += self.getLastDayOfMonth(i)
        # Adderar resterande dagar
        sum_days += day-1
        return sum_days
    
    def getLeapDays(self):
        """ Returnerar antalet skottdagar sedan 1900 fram till givet år – d.v.s. det givna året inkluderas ej.
        
        Returnerar:
            (int): antalet skottdagar sedan 1900.
        """
        count_leap_days = 0
        for i in range(self.MIN_YEAR, self.year):
            if self.isLeapYear(i):
                count_leap_days += 1
        return count_leap_days
        

class Holiday:
    """ Klassen 'Holiday' tar fram vilka helger som infaller för en specifik kalendermånad.
    """
    def __init__(self, date):
        """ Konstruktorn för klassen 'Holiday'.
        
        Argument:
            date (Date): består av objektet 'Date(year, month)' som håller koll på kalendermånaden för vald år och månad.
        """
        self.date = date

class Calendar:
    """ Klassen 'Calendar' är själva huvudklassen för kalendern och tar fram kalendern för vald månad och år.
    """
    def __init__(self):
        """ Konstruktorn för klassen Calendar.
        """
        self.names_of_the_week = ["Må","Ti","On","To","Fr","Lö","Sö"] # 0-6 (må-sö)
        self.names_of_the_month = { # månaders namn med index 1-12 (jan-dec)
                                1:"januari", 2:"februari", 3:"mars",
                                4:"april", 5:"maj", 6:"juni", 7:"juli",
                                8:"augusti", 9:"september", 10:"oktober",
                                11:"november", 12:"december"
                            }
        self.setDate(1900, 1) # Startdatum
    
    def setDate(self, year, month):
        """ Ändrar datumet för kalendermånad.
        
        Argument:
            year  (int): heltal motsvarande årtalet mellan intervallet 1900-3000.
            month (int): heltal motsvarande månaden mellan intervallet 1-12 (jan-dec).
        """
        self.year = year
        self.month = month
        self.date = Date(self.year, self.month)
        self.holidays = Holiday(self.date)
        self.space = 1 # Antalet blanksteg vid utskrift mellan kalenderdagarna.
    
    def getCalendarHead(self):
        """ Returnerar kalenderns rubrik för månaden och veckodagar
        
        Argument:
            space (int): heltal mellan 1 och uppåt som motsvarar antalet blanksteg mellan kalenderdagarna
        """
        # Titeln för månadskalendern
        calendar_head = self.names_of_the_month[self.month] + " " + str(self.year) + "\n"
        # Titeln för veckodagar
        for i in range(7):
            calendar_head += self.names_of_the_week[i]
            if i < 6:
                calendar_head += " "*self.space
        
        return calendar_head
    
    def getCalendarBody(self):
        """ Returnerar kalenderkroppen, dvs. dagarna för aktuell månad.
        
        Returnerar:
            (list): returnerar lista med längden 7x(([sista dagen på månaden]-1)//7+1)
                    där index 0 mostvarar måndag på första månadsveckan.
        """
        days = [i for i in range(1,self.date.getLastDayOfMonth(self.month)+1)]
        if self.date.getDayOfTheWeek(1) > 0:
            days = [0]*self.date.getDayOfTheWeek(1) + days
        
        while len(days)%7 != 0:
            days += [0]
        
        return days
    
    def printCalendar(self):
        """ Skriver ut i konsolen själva kalendern med titel och månadens dagar.
        """
        print(self.getCalendarHead())
        cal_body = self.getCalendarBody()
        for i in range(len(cal_body)):
                if cal_body[i] == 0:
                    print("  ", end="")
                elif cal_body[i] <= 9:
                    print(" " + str(cal_body[i]), end="")
                else:
                    print(cal_body[i], end="")
                 
                if (i+1)%7 == 0:
                    print("", end="\n")
                else:
                    print("", end=" "*self.space)


### Huvudprogrammet ###

def main():
    cal = Calendar()
    print("\tKalenderprogram")
    while True:
        while True:
            print("(1) Se denna månadskalender")
            print("(2) Ange år och månad")
            menu = int(input("Välj ett alterantiv (1-2): "))
            if 1 <= menu <= 2:
                break
        while True:
            if menu == 2:
                while True:
                    year = int(input("Ange det år du vill titta på: "))
                    if cal.date.MIN_YEAR <= year <= cal.date.MAX_YEAR:
                        break
                while True:
                    month = int(input("Ange numret på den månad du vill titta på (1-12): "))
                    if 1 <= month <= 12:
                        cal.setDate(year, month)
                        break
            else:
                now = localtime()
                cal.setDate(now[0], now[1])
            
            cal.printCalendar()
            break

if __name__ == "__main__":
    main()
