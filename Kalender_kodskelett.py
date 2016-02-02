# -*- coding: UTF-8 -*-
from time import *

# Titel: 110 Kalender
# Författare: Andreas Poremski
# Datum: 2016-01-29
#
# Program som skriver ut en kalender för ett godtyckligt år i intervallet 1900 och 3000.

# Kalender hanterare
class CalendarHandler:
    def __init__(self):
        """ Konstruktorn för kalender hanteraren
        """
        self.MINIMUM_YEAR = 1900 # Det lägasta året man kan generera.
        self.MAXIMUM_YEAR = 3000 # Det högasta året man kan generera.
        self.FIRST_DAY = 1 # Första kalenderdagenden 1/1-1900 – intervall 0-6 (sön-lör).
    
    def isLeapYear(self, year):
        """ Kollar om ett år är skottår eller ej.
        
        Argument:
            year (int): heltal motsvarande årtalet mellan intervallet 1900-3000.
        
        Returnerar:
            (boolean): skottår ger True, annars False
        """
        return False
    
    def getDaysInEachMonth(self, year):
        """ Returnerar lista med antalet dagar per månad.
        
        Argument:
            year (int): heltal motsvarande årtalet mellan intervallet 1900-3000.
            
        Returnerar:
            (list): lista med 12 element av typen 'int' där index 0 motsvaras av januari och index 11 av december.
        """
        return [0,0,0,0,0,0,0,0,0,0,0,0]
    
    def getLeapDays(self, year):
        """ Returnerar antalet skottdagar sedan 1900 fram till ett agivet år i konstruktorn – d.v.s.
            det givna året inkluderas ej.
        
        Argument:
            year (int): heltal motsvarande årtalet mellan intervallet 1900-3000.
        
        Returnerar:
            (int): antalet skottdagar sedan 1900.
        """
        return 0
    
    def getDay(self, year, month, day):
        """ Ger veckodagen för det angivna datumet.
        
        Argument:
            year (int): heltal motsvarande årtalet mellan intervallet 1900-3000.
            month (int): heltal motsvarande månaden mellan intervallet 1-12 (jan-dec).
            day (int): heltal motsvarande kalenderdagen mellan intervallet 1-31.
        
        Returnerar:
            (int): siffra mellan 0 och 6 där 0 motsvaras av söndag och 6 av lördag.
        """
        return 0
    
    def getDayDuration(self):
        """ Ger antalet dagar sedan 1900-01-01 fram till givet datum i konstruktorn;
            det givna dagen inkluderas ej.
        
        Returnerar:
            (int): antalet dagar sedan 1900-01-01.
        """
        return 0

# Själva kalenderklassen
class Calendar:
    def __init__(self):
        """ Konstruktorn för kalendern
        """
        self.monthNames = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktover", "november", "december"]
        self.dayNames = ["Sö", "Må", "Ti", "On", "To", "Fr", "Lö"]
        self.year = 1900
        self.month = 1
        handler = CalendarHandler()
        self.MAX_YEAR = handler.MAXIMUM_YEAR
        self.MIN_YEAR = handler.MINIMUM_YEAR
    
    def printMonth(self, year, month):
        """ Skriver ut kalendern för given månad och år.
        
        Argument:
            year (int): årtal mellan 1900 och 3000
            month (int): månad mellan 1 och 12, där 1 år januari och 12 är december.
        """
        pass

# Huvudprogrammet
def main():
    pass
'''
    cal = Calendar()
    
    # Meny 1
    now = localtime()
    cal.printMonth(now[0], now[1])
    
    # Meny 2
    year = int(input("År: "))
    month = int(input("Månad: "))
    cal.printMonth(year, month)
'''

main()
