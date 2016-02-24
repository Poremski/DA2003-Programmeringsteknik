# Titel: 110 Kalender
# Författare: Andreas Poremski
# Datum: 2016-02-23
# Python: 3.5.1
#
# Ett kalenderprogram för åren mellan 1900 till och med 3000.

import os
import platform
from tkinter import *
from tkinter import messagebox as msg
from tkinter.ttk import *
from time import localtime


class Calendar(object):
    """
    Huvudklass för kalendern som hanterar grundläggande uträkningar.

    """
    DAYS = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lördag', 'Söndag']
    MONTHS = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli',
              'Augusti', 'September', 'Oktober', 'November', 'December']
    MIN_YEAR, MAX_YEAR = 1900, 3000

    def __init__(self):
        """
        Konstruktorn som ställer in nuvarande år och månad.
        """
        self.year, self.month = localtime()[0], localtime()[1]

    @staticmethod
    def get_short_days(char: int = 2) -> list:
        """
        Returnerar lista med veckodagar i kortform.

        :param char: Heltal som motsvarar antalet bokstäver som veckonamnen
                     ska bestå av. Som förvalt är det två bokstäver.
        :return: Lista med veckodagar förkortade till givet via 'char' antal bokstäver.
        """
        return [days[:char] if len(days) >= char else days for days in Calendar.DAYS]

    @staticmethod
    def get_short_months(char: int = 3) -> list:
        """
        Returnerar lista med årets månader i kortform.

        :param char: Heltal som motsvarar antalet bokstäver som månadsnamnen
                     ska bestå av. Som förvalt är det tre bokstäver.
        :return: Lista med årets månader förkortade till givet via 'char' antal bokstäver.
        """
        return [months[:char] if len(months) >= char else months for months in Calendar.MONTHS]

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Returnerar om det givna året är ett skottår eller ej.

        :param year: Heltal motsvarande året mellan intervallet 1900 och 3000.
        :return: Boolesk datatyp där skottår är 'True', annars 'False'.
        """
        return (year % 4 is 0 and year % 100 is not 0) or year % 400 == 0

    @staticmethod
    def get_last_day_of_month(year: int, month: int) -> int:
        """
        Returnerar en given månads sista dag.

        :param year: Heltal motsvarande året mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Heltal mellan 28 och 31 som motsvarar sista dagen för en given månad.
        """
        DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 0-11 (jan-dec)
        if not Calendar.is_leap_year(year) or month is not 2 and Calendar.is_leap_year(year):
            return DAYS_IN_MONTH[month-1]
        else:
            return 29

    @staticmethod
    def get_leap_years(year: int) -> int:
        """
        Returnerar antalet skottår sedan 1900 fram till det givna året,
        där det givna året exkluderas i beräkningen.

        :param year: Heltal motsvarande året mellan intervallet 1900 och 3000.
        :return: Heltal som motsvarar antalet skottår.
        """
        counter = 0
        for y in range(Calendar.MIN_YEAR, year):
            if Calendar.is_leap_year(y):
                counter += 1
        return counter

    @staticmethod
    def get_duration_in_days(year: int, month: int, day: int) -> int:
        """
        Returnerar antalet dagar som har fortskridit sedan 1900-01-01 fram till
        den givna dagen. Given dag exkluderas i beräkningen.

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :param day: Heltal motsvarande kalenderdagen mellan intervallet 1-28, 29, 30 eller 31.
        :return: Heltal bestående av summan av antalet dagar sedan 1900-01-01.
        """
        # År till dagar
        sum_days = (year - Calendar.MIN_YEAR)*365 + Calendar.get_leap_years(year)
        # Månader till dagar
        if month >= 2:
            for i in range(1, month):
                sum_days += Calendar.get_last_day_of_month(year, i)
        # Adderar resterande dagar
        sum_days += day-1
        return sum_days

    @staticmethod
    def get_day_of_the_week(year: int, month: int, day: int) -> int:
        """
        Returnerar heltal motsvarades veckodagen för det givna datumet mellan 0-6 (må-sö).

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :param day: Heltal motsvarande kalenderdagen mellan intervallet 1-28, 29, 30 eller 31.
        :return: Returnerar heltal mellan 0 och 6, där 0 är måndag och 6 är söndag.
        """
        return (Calendar.get_duration_in_days(year, month, day)) % 7

    @staticmethod
    def get_list_of_month(year: int, month: int) -> list:
        """
        Returnerar en lista med månadens dagar.

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Lista med längden 7*(([sista dagen på månaden]-1)//7+1) där
                 index 0 motsvaras av måndagen på första månadsveckan.
        """
        days = [day for day in range(1, Calendar.get_last_day_of_month(year, month)+1)]
        days = [0]*Calendar.get_day_of_the_week(year, month, 1) + days  # Eventuell förskjutning av första dagen.
        while len(days) % 7 != 0:
            days += [0]  # Avslutar listan för att uppnå längden 7x(([sista dagen på månaden]-1)//7+1).
        return days

    @staticmethod
    def get_matrix_of_month(year: int, month: int) -> list:
        """
        Returnerar en matris med månadens dagar.

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Lista med längden 7 och antalet ([sista dagen på månaden]-1)//7+1 där
                 index [0][0] motsvaras av måndagen på första månadsveckan,
                 index [0][6] motsvaras av söndagen på första månadsveckan,
                 index [1][0] motsvaras av måndagen på andra månadsveckan och
                 index [1][6] motsvaras av söndagen på andra månadsveckan o.s.v.
        """
        list_days = Calendar.get_list_of_month(year, month)
        matrix_days = []
        for i in range(0, len(list_days), 7):
            matrix_days.append(list_days[i:i+7])
        return matrix_days

    @staticmethod
    def remove_duplicates(values: list) -> list:
        """
        Rensar bort dubbletter i listan så att endast unika värden kvarstar.

        :param values: Lista innehållandes värden som ska filtreras.
        :return: En filtrerad lista där endast unika värden finns representerade.
        """
        output = []
        seen = set()
        for value in values:
            if value not in seen:
                output.append(value)
                seen.add(value)
        output.sort()
        return output

    @staticmethod
    def get_holidays(year: int, month: int) -> list:
        """
        Returnerar en lista bestående av heltal som motsvaras av röda dagar för den givna månaden.

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Lista innehållandes helgdagar för den givna månad.
        """
        days = []
        holidays = Holiday(year).get_month(month)
        for i in range(len(holidays)):
            days.append(holidays[i]['day'])
        return Calendar.remove_duplicates(days)

    @staticmethod
    def get_holidays_with_names(year: int, month: int) -> list:
        """
        Returnerar en lista bestående av lexikonelement innehållandes elementen
        'day' och 'name' för röda dagar (ej traditionella söndagar) för den givna månaden.

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Lista innehållandes lexikon bestående av helgdagar för det givna månaden.
        """
        holidays = Holiday(year).get_month(month)
        container = []
        for i in range(len(holidays)):
            # Traditionella söndagar har elementet 'type', vilket de övriga röda dagarna inte har.
            if 'type' not in holidays[i]:
                day = holidays[i]['day']
                name = holidays[i]['name']
                container.append({'day': day, 'name': name})
        return container


class CalendarText(Calendar):
    """
    Underklass för kalender med anpassning för textbaserad användargränssnitt (TUI).
    """
    def __init__(self, year: int = None, month: int = None, date_now: bool = False):
        """
        Sätter år och månad för kalendervisning.

        :param year: Heltal motsvarande årtal mellan intervallet 1900 och 3000.
        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :param date_now: 'True' ignorerar attributerna 'year' och 'month' och
                         tillämpar värdena för år och månad från huvudklassens
                         konstruktor som innehåller dagens värde för år och månad.
                         'False' skriver över huvudklassens attributargument med
                         attributerna 'year' och 'month'.
        """
        super().__init__()
        if date_now is False:
            self.year = year
            self.month = month

    def print_month(self):
        """
        Skriver ut given kalendermånad i konsolen.
        """
        title = str(self.MONTHS[self.month-1]).lower() + ' ' + str(self.year)
        decoprint(title.center(20), ['bold'])  # Titel
        decoprint(' '.join(self.get_short_days()), ['bold'])  # Veckodagar
        print(self.get_calendar_body())  # Kalenderkroppen
        self.print_holidays()

    def get_calendar_body(self) -> str:
        """
        Genererar fram en textbaserad kalenderkropp för given månad.

        :return: Returnerar en textsträng med en kalenderkropp
        """
        cal = ''
        holidays = self.get_holidays(self.year, self.month)
        for w, week in enumerate(self.get_matrix_of_month(self.year, self.month)):
            for d, day in enumerate(week):
                if day:
                    if day in holidays:
                        if day >= 10:
                            cal += deco(str(day), ['red'])
                        else:
                            cal += deco(' ' + str(day), ['red'])
                    elif day >= 10:
                        cal += str(day)
                    else:
                        cal += ' ' + str(day)
                else:
                    cal += ' '*2
                cal += ' '
            cal += '\n'
        return cal

    def print_holidays(self):
        """
        Skriver ut helgdagar för kalendermånaden i konsolen,
        där traditionell söndag inte skrivs ut.
        """
        holidays = self.get_holidays_with_names(self.year, self.month)
        if len(holidays) > 0:
            print('Aktuella helger den här månaden:')
            for holiday in holidays:
                print(str(holiday['day']) + '/' + str(self.month), str(holiday['name']))
            print('', end='\n')


class CalendarGUI(Calendar):
    """
    Underklass för kalendern med anpassning för grafisk användargränsnitt (GUI).
    """
    def get_month(self, month: int) -> str:
        """
        Returnerar kortform av månadsnamnet för given månad.

        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Textsträng med det förkortade månaden för given månad.
        """
        return self.get_short_months()[month-1]


class Holiday:
    """
    Räknar ut när helgdagar infaller under givet år.
    """
    def __init__(self, year: int):
        self.year = year
        self.easter = self.get_easter_sunday()
        self.__holidays = {}
        for m in range(1, 13):
            self.__holidays[m] = []
        self.add_holidays()

    def add_holidays(self):
        """
        Bokför samtliga helger.
        """
        # Rörliga helger
        self.add_good_friday('Långfredag')
        self.add_easter_sunday('Påskdagen')
        self.add_easter_monday('Annadag påsk')
        self.add_ascension_day('Kristi himmelsfärdsdag')
        self.add_pentecost('Pingsdag')
        self.add_midsummer('Midsommardag')
        self.add_all_hallows('Alla helgons dag')

        # Fasta helger
        self.add_sundays()  # Alla söndagar
        self.add_holiday_manually(month=1, day=1, name='Nyårsdagen')
        self.add_holiday_manually(month=1, day=6, name='Trettondagen')
        self.add_holiday_manually(month=5, day=1, name='1:a maj')
        self.add_holiday_manually(month=6, day=6, name='Sveriges nationaldag')
        self.add_holiday_manually(month=12, day=25, name='Juldagen')
        self.add_holiday_manually(month=12, day=26, name='Annandag')

    def add_holiday_manually(self, month: int, day: int, name=None):
        """
        Markerar ett valt datum som röd dag.

        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :param day: Heltal motsvarande kalenderdagen mellan intervallet 1-28, 29, 30 eller 31.
        :param name: Namnet på helgen.
        """
        self.__holidays[month].append({'day': day, 'name': name})

    def add_sundays(self, name=None):
        """
        Markerar alla söndagar för året som röda dagar.

        :param name: Namnet på helgen.
        """
        for month in range(1, 13):
            for day in range(1, Calendar.get_last_day_of_month(self.year, month)+1):
                if Calendar.get_day_of_the_week(self.year, month, day) is 6:
                    self.__holidays[month].append({'day': day, 'name': name, 'type': 'sunday'})

    def add_midsummer(self, name=None):
        """
        Markerar midsommardagen som röd dag.
        Den infaller på en lördag i intervallet 20 - 26 juni.

        :param name: Namnet på helgen.
        """
        weekday = Calendar.get_day_of_the_week(self.year, 6, 20) % 7
        if weekday == 5:
            self.add_holiday_manually(month=6, day=20, name=name)
        elif weekday < 5:
            self.add_holiday_manually(month=6, day=21+(4-weekday), name=name)
        else:
            self.add_holiday_manually(month=6, day=26, name=name)

    def add_all_hallows(self, name=None):
        """
        Markerar alla helgons dag som röd dag.
        Infaller på en lördag i intervallet 31 okt. - 6 nov.

        :param name: Namnet på helgen.
        """
        weekday = Calendar.get_day_of_the_week(self.year, 10, 31) % 7
        if weekday == 5:
            self.add_holiday_manually(month=10, day=31, name=name)
        elif weekday < 5:
            self.add_holiday_manually(month=11, day=1+(4-weekday), name=name)
        else:
            self.add_holiday_manually(month=11, day=6, name=name)

    def add_easter_sunday(self, name=None) -> dict:
        """
        Markerar påskdagen som röd dag.

        :param name: Namnet på helgen.
        """
        m, d = self.easter['month'], self.easter['day']
        self.add_holiday_manually(month=m, day=d, name=name)

    def get_easter_sunday(self) -> dict:
        """
        Returnerar påskdagens infallande för det givna året.

        :return: Lexikon med elementen 'month' och 'day' för påskdagens infallande.
        """
        # Algoritmen för uträkning kommer från instruktionerna för projektuppgiften.
        y = self.year  # Årtalet
        c = (y//100)+1  # Århundradet
        g = (y % 19)+1  # Gyllene talet
        x = ((3*c)//4)-12  # Antalet överhoppade skottdagar
        z = ((8*c+5)//25)-5  # Månkorrektionen
        e = (11*g+20+z-x) % 30  # Epakten E, solårets överskott över månåret
        if e is 25 and g > 11 or e == 24:
            e += 1
        n = 44-e  # Fullmånen
        if n < 21:
            n += 30
        d = ((5*y)//4)-x-10  # Söndagstalet
        s = n+7-((d+n) % 7)  # Första söndagen efter fullmåne
        if s > 31:
            return {'month': 4, 'day': s-31}
        else:
            return {'month': 3, 'day': s}

    def add_easter_monday(self, name=None):
        """
        Markerar Annandag påsk som röd dag.
        Den infaller dagen efter påskdagen.

        :param name: Namnet på helgen.
        """
        m, d = self.easter['month'], self.easter['day']
        if d < Calendar.get_last_day_of_month(self.year, m):
            self.add_holiday_manually(month=m, day=d+1, name=name)
        else:
            self.add_holiday_manually(month=m+1, day=1, name=name)

    def add_ascension_day(self, name=None):
        """
        Markerar Kristi himmelsfärdsdagen som röd dag.
        Den infaller 39 dagar efter påskdagen.

        :param name: Namnet på helgen.
        """
        date = self.get_date_after(39)
        m, d = date['month'], date['day']
        self.add_holiday_manually(month=m, day=d, name=name)

    def add_pentecost(self, name=None):
        """
        Markerar Pingstdagen som röd dag.
        Den infaller 49 dagar efter påskdagen.

        :param name: Namnet på helgen.
        """
        date = self.get_date_after(49)
        m, d = date['month'], date['day']
        self.add_holiday_manually(month=m, day=d, name=name)

    def get_date_after(self, days: int) -> dict:
        """
        Räknar antal dagar (under samma år) framåt i tiden från påskdagen.

        :param days: Antalet dagar som man vill räkna framåt i tiden.
        :return: Returnerar lexikon med elementet 'month' och 'day'.
        """
        m, d = self.easter['month'], self.easter['day']
        count = days
        while count > 0:
            count -= 1
            if d < Calendar.get_last_day_of_month(self.year, m):
                d += 1
            else:
                d = 1
                m += 1
        return {'month': m, 'day': d}

    def add_good_friday(self, name=None):
        """
        Markerar Långfredagen som röd dag.
        Den infaller två dagar innan påskdagen.

        :param name: Namnet på helgen.
        """
        m, d = self.easter['month'], self.easter['day']
        if d >= 3:
            self.add_holiday_manually(month=m, day=d-2, name=name)
        else:  # Långfredagen infaller på föregående månad
            d = Calendar.get_last_day_of_month(self.year, m-1)+d-2
            self.add_holiday_manually(month=m-1, day=d, name=name)

    def get_month(self, month: int) -> list:
        """
        Returnerar en lista med helgdagar för en given månad.

        :param month: Heltal motsvarande månaden mellan intervallet 1 och 12 (jan-dec).
        :return: Lista innehållandes helgdagar för given månad.
        """
        return self.__holidays[month]


class Application:
    """
    Klassen för den grafiska användargränsnittet för kalenderprogrammet.
    """
    def __init__(self, master: Tk, app_name: str):
        """
        Konstruktorn för GUI-applikationen avseende kalenderprogrammet.

        :param master: Konstruktorn för GUI-hanteraren Tkinter
        :param app_name: Sträng bestående av applikationens namn.
        """
        self.master = master
        self.app_name = app_name
        self.master.title(self.app_name)
        self.master.geometry('+200+200')  # Förskjuter fönstret för att inte hamna högst upp i vänstra kanten.
        self.cal = CalendarGUI()
        self.year = self.cal.year
        self.month = self.cal.month

        self.tabs = None  # Innehåller Notebook-objekten.
        self.style = Style()  # Behållare för applicering av utsmyckning av objektelement.
        self.widgets = []  # Innehåller referenser till objekt som ska rensas vid fönsteruppdatering.
        self.year_entry = None  # Skrivfältet för årtal
        self.month_entry = None  # Skrivfältet för månad

        self.__menu()   # Menyn för programmet
        self.__main_container()  # Huvudkroppen

    def __main_container(self):
        """
        Huvudkroppen för programmet innehållandes första lagret (Frame) i programmet.
        """
        self.style.configure('HEADER.TLabel', height=2)
        self.style.configure('BTN_SM.TButton', width=2)

        main_frame = Frame(self.master)
        self.widgets.append(main_frame)
        main_frame.grid()
        Label(main_frame, text='År:').grid(row=0, column=0, columnspan=2)

        self.year_entry = Entry(main_frame, width=5, justify=CENTER)
        self.year_entry.grid(row=0, column=2, columnspan=2)
        self.year_entry.insert(0, str(self.year))

        Label(main_frame, text='Månad:').grid(row=0, column=4, columnspan=2)

        self.month_entry = Entry(main_frame, width=5, justify=CENTER)
        self.month_entry.grid(row=0, column=6, columnspan=2)
        self.month_entry.insert(0, str(self.month))

        Button(main_frame, text='OK', command=self.__do_select_month,
               style='BTN_SM.TButton').grid(row=0, column=8, columnspan=1)

        Button(main_frame, text='«', command=self.__do_reverse_one_month,
               style='BTN_SM.TButton').grid(row=1, column=2, columnspan=1)

        Label(main_frame, text=self.cal.get_month(self.month) + ' ' + str(self.year),
              style='HEADER.TLabel').grid(row=1, column=3, columnspan=4)

        Button(main_frame, text='»', command=self.__do_forward_one_month,
               style='BTN_SM.TButton').grid(row=1, column=7, columnspan=1)

        self.tabs = Notebook(main_frame)
        self.__calendar_frame('Kalender')
        self.__holiday_frame('Röda dagar')
        self.tabs.grid(row=2, columnspan=9)

    def __calendar_frame(self, name: str):
        """
        Lager för fliken 'Kalender'.

        :param name: Namn på fliken.
        """
        self.style.configure('DAYBTN.TButton', width=2)
        self.style.configure('DAYBTN_RED.TButton', width=2, foreground='red')

        self.calendar_frame = Frame(self.tabs)
        for nbr, day in enumerate(self.cal.get_short_days()):
            days_lbl = Label(self.calendar_frame, text=day)
            self.widgets.append(days_lbl)
            days_lbl.grid(row=0, column=nbr)
        cal = Calendar.get_matrix_of_month(self.year, self.month)
        holiday = Calendar.get_holidays(self.year, self.month)
        for w, week in enumerate(cal):
            for d, day in enumerate(week):
                if day:
                    if day in holiday:
                        day_btn = Button(self.calendar_frame, text=day, style='DAYBTN_RED.TButton')
                    else:
                        day_btn = Button(self.calendar_frame, text=day, style='DAYBTN.TButton')
                    self.widgets.append(day_btn)
                    day_btn.grid(row=w+1, column=d)
        self.tabs.add(self.calendar_frame, text=name)

    def __holiday_frame(self, name: str):
        """
        Lager för fliken 'Röda dagar'.
        :param name: Namnet på fliken
        """
        self.holidays_frame = Frame(self.tabs)

        row_count = 1
        holidays = self.cal.get_holidays_with_names(self.year, self.month)
        for holiday in holidays:
            Label(self.holidays_frame, text=str(holiday['day'])).grid(row=row_count, column=0)
            Label(self.holidays_frame, text=self.cal.get_month(self.month).lower()).grid(row=row_count, column=1)
            Label(self.holidays_frame, text=str(holiday['name'])).grid(row=row_count, column=2)
            row_count += 1

        if row_count > 1:
            Label(self.holidays_frame, text='Aktuella helger denna månad:').grid(row=0, column=0, columnspan=3)
        else:
            Label(self.holidays_frame, text='Inga helger denna månad.').grid(row=0, column=0, columnspan=3)

        self.tabs.add(self.holidays_frame, text=name)

    def __menu(self):
        """
        Menyn för programmet
        """
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Arkiv', menu=file_menu)
        # Anpassar menyn efter operativsystemes traditionella menystruktur.
        if platform.system() in ['Windows', 'Linux']:
            help_menu = Menu(menu, tearoff=0)
            menu.add_cascade(label='Hjälp', menu=help_menu)
            help_menu.add_command(label='Om...', command=self.__about_dlg)
        else:
            file_menu.add_command(label='Om...', command=self.__about_dlg)
            file_menu.add_separator()
        file_menu.add_command(label='Avsluta', command=self.master.quit)

    def __about_dlg(self):
        """
        Dialogfönsret "Om…".
        """
        about = Toplevel()
        about.title('Om ' + self.app_name)
        about.resizable(FALSE, FALSE)
        about.geometry('+200+200')  # Förskjuter fönstret för att inte hamna högst upp i vänstra kanten.

        # Består av en GIF-bild omkodad till skrivbar 7-bitars ASCII-tecken (base64)
        IMG_DATA = 'R0lGODlhQABAALMPAPj8/aexuZjT7sTl9Vlse1+95eTz+XvI6Sux4ACj2+vu8MLJzgC' \
                   'Y1pOfqRw8UP///yH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPS' \
                   'JXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZ' \
                   'G9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxMTEgNzku' \
                   'MTU4MzI1LCAyMDE1LzA5LzEwLTAxOjEwOjIwICAgICAgICAiPiA8cmRmOlJERiB4bWx' \
                   'uczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucy' \
                   'MiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6L' \
                   'y9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRv' \
                   'YmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmN' \
                   'vbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG' \
                   '9iZSBQaG90b3Nob3AgQ0MgMjAxNSAoTWFjaW50b3NoKSIgeG1wTU06SW5zdGFuY2VJR' \
                   'D0ieG1wLmlpZDo4RkU0RDYwNENDRjIxMUU1QkM3MThBMTBDRENGMjk0QiIgeG1wTU06' \
                   'RG9jdW1lbnRJRD0ieG1wLmRpZDo4RkU0RDYwNUNDRjIxMUU1QkM3MThBMTBDRENGMjk' \
                   '0QiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOj' \
                   'k3MTQ5M0ZGQ0NDNTExRTVCQzcxOEExMENEQ0YyOTRCIiBzdFJlZjpkb2N1bWVudElEP' \
                   'SJ4bXAuZGlkOjk3MTQ5NDAwQ0NDNTExRTVCQzcxOEExMENEQ0YyOTRCIi8+IDwvcmRm' \
                   'OkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5' \
                   'kPSJyIj8+Af/+/fz7+vn49/b19PPy8fDv7u3s6+rp6Ofm5eTj4uHg397d3Nva2djX1t' \
                   'XU09LR0M/OzczLysnIx8bFxMPCwcC/vr28u7q5uLe2tbSzsrGwr66trKuqqainpqWko' \
                   '6KhoJ+enZybmpmYl5aVlJOSkZCPjo2Mi4qJiIeGhYSDgoGAf359fHt6eXh3dnV0c3Jx' \
                   'cG9ubWxramloZ2ZlZGNiYWBfXl1cW1pZWFdWVVRTUlFQT05NTEtKSUhHRkVEQ0JBQD8' \
                   '+PTw7Ojk4NzY1NDMyMTAvLi0sKyopKCcmJSQjIiEgHx4dHBsaGRgXFhUUExIREA8ODQ' \
                   'wLCgkIBwYFBAMCAQAAIfkEAQAADwAsAAAAAEAAQAAABP/wyUmrvTjrzbv/YCiOZGmea' \
                   'KqubOu+MEEAnExv9us4Crf3m5+O5yMGjSNFoMFsNh6/pXMKiE6pv2sjAMw0duAwlBcu' \
                   '/87msAKdfmK+DoJ2rNQ2qzypHa/QEnZuFWsOCxh8G4caiRYLQhUBcRl/cV0XkwSVFpe' \
                   'ZE38BFl+BFY1gnxikO6YXqA6qFaGgDqIUrK6jYba0uG+ysbMTAJcGGcE7BMOGwry/sI' \
                   'YLCzfEz9HO0F69r9gwIs0U3dsg3xJwaeXm5+jmzOns7e6AvuDc2hPi8hz29vca+fT7G' \
                   '/1+WRBQYMCEAQUnGBBgUMLChg8eKjxwgNo4fw/0UTDAgEECGhz/O9IAkKAjMgQdG6Jk' \
                   '0LBARwHxsgnc2PFjxI4MRuJEVpKlhJ4tX8b0htECQohHJwhAAFPCAAQVnUK9YYCixYw' \
                   'YNf4bWg8jAGQSvlYA65CaAbPUAFzFum6WgZIHwqIsIJcBggkuEdw44HGvR2QC/nK9OG' \
                   'tATac4Qe58AABnQ6A/hT5Y2ZRo27Fww5akyxilXgkubT4IjYxvAsAmB7O1IBbYWdfRv' \
                   'qLdOFu11q2WVRNEKgDsQt8MFQZ3OJyxgMq5ZVYw7NFhTZ19Gfc8mVLCyqAMkBMezPzu' \
                   'A+Y5b6ZunPoBZPPVR0tOzl7pAbBLIS6tPP/gVKlRIyIocDUgbnxZYWTAfACxEQiMgWE' \
                   'heIJ/G22mmV0PfjZZdAsGWNhh3yUmHgPDkOdThZdRAABKTY3IQFygMcDZA3xJaAKDFV' \
                   'gkY4wqwPjfMhZAQsCNGnhiwSCF8MiII9nEYceRSCaJ5CQzYfXOk1A2KUEdSlZppR1cC' \
                   'Knlllx26eWXYIYp5pg8RgAAOw=='
        img = PhotoImage(data=IMG_DATA)
        logo = Label(about, image=img)
        logo.image = img
        logo.grid(row=1, column=0)

        self.style.configure('TITLE.TLabel', padx=10, pady=10, weight='bold')
        self.style.configure('TXTMSG.TLabel', justify=LEFT, padx=10, pady=10)
        self.style.configure('CLOSE.TButton', pady=10)

        Label(about, text=self.app_name, style='TITLE.TLabel').grid(row=0, columnspan=2)

        txtmsg = 'Det här är ett kalenderprogram som tar fram en månadskalender\n' \
                 'mellan årtalsintervallet 1900 och 3000.\n\n' \
                 'Kalenderprogrammet är en del av en inlämningsuppgift för webbkursen\n' \
                 'DA2003 (Programmeringsteknik) vid Stockholms universitet.\n\n' \
                 'Namn: Andreas Poremski\n' \
                 'Datum: 2016-02-23'
        Label(about, text=txtmsg, style='TXTMSG.TLabel').grid(row=1, column=1)

        Button(about, text='Stäng', command=about.destroy, style='CLOSE.TButton').grid(row=2, columnspan=2)

    def __do_forward_one_month(self):
        """
        Hoppar framåt en månad i kalendern.
        """
        current_frame = self.tabs.tab(self.tabs.select(), 'text')
        if self.month < 12:
            self.month += 1
        else:
            self.year += 1
            self.month = 1
        self.__clear_widgets()
        self.__main_container()
        if current_frame != 'Kalender':
            self.tabs.select(1)
        else:
            self.tabs.select(0)

    def __do_reverse_one_month(self):
        """
        Hoppar bakåt en månad i kalendern.
        """
        current_frame = self.tabs.tab(self.tabs.select(), 'text')
        if self.month > 1:
            self.month -= 1
        else:
            self.year -= 1
            self.month = 12
        self.__clear_widgets()
        self.__main_container()
        if current_frame != 'Kalender':
            self.tabs.select(1)
        else:
            self.tabs.select(0)

    @staticmethod
    def __is_integer(attr):
        """
        Kontrollerar om attributet är heltal och returnerar sant eller falskt.

        :param attr: Attributet som ska verifieras.
        :return: 'True' vid heltal, annars 'False'.
        """
        try:
            int(attr)
        except ValueError:
            return False
        else:
            return True

    def __do_select_month(self):
        """
        Hoppar till given kalendermånad för givet år.
        """
        year = self.year_entry.get()
        month = self.month_entry.get()

        if not self.__is_integer(year):
            if not self.__is_integer(month):
                msg.showerror('Felaktigt årtal och månad!', 'Ange årtalet i heltal mellan ' +
                              str(self.cal.MIN_YEAR) + ' och ' + str(self.cal.MAX_YEAR) + ' samt ' +
                              'månaden i siffror mellan 1 och 12.')
            else:
                msg.showerror('Felaktigt årtal!', 'Ange  årtalet i heltal mellan ' + str(self.cal.MIN_YEAR) +
                              ' och ' + str(self.cal.MAX_YEAR) + '.')
        elif not self.__is_integer(month):
            msg.showerror('Felaktig månad!', 'Ange månaden i siffror mellan 1 och 12.')
        elif not self.cal.MIN_YEAR <= int(year) <= self.cal.MAX_YEAR:
            if not 1 <= int(month) <= 12:
                msg.showerror('Felaktigt årtal och månad!', 'Det angivna året ' + year +
                              ' och månaden ' + month + ' är felaktiga. ' + 'Ange årtalet i heltal mellan ' +
                              str(self.cal.MIN_YEAR) + ' och ' + str(self.cal.MAX_YEAR) + ' samt ' +
                              'månaden i siffror mellan 1 och 12.')
            else:
                msg.showerror('Felaktigt årtal!', 'Det angivna året ' + year + ' är felaktigt. ' +
                              'Ange årtalet i heltal mellan ' + str(self.cal.MIN_YEAR) + ' och ' +
                              str(self.cal.MAX_YEAR))
        elif not 1 <= int(month) <= 12:
            msg.showerror('Felaktig månad!', 'Den angivna månaden ' + month + ' är felaktig. ' +
                          'Ange månaden i siffror mellan 1 och 12.')
        else:
            self.year = int(year)
            self.month = int(month)
            self.__clear_widgets()
            self.__main_container()

    def __clear_widgets(self):
        """
        Rensar listan 'widgets' för att ta bort referensen till
        Tkinter-objekten som finns i metoden 'calendar_body'.
        """
        for widget in self.widgets[:]:
            widget.destroy()


def deco(text: str, attrs: list = None) -> str:
    """
    Returnerar en typografisk dekorerad textsträng.

    :param text:  Textsträngen som ska dekoreras.
    :param attrs: En lista bestående av följande textelement, där
                  ingen speciell ordning på attributen i listan
                  behöver beaktas:
                      bold        - för fettstild text
                      underline   - för understruken text
                      red         - för röd text
    :return: Den dekorerade textsträngen returneras.

    Exempel:
        txt = deco('en text', ['bold', 'red'] - för att få röd fettstild text
    """
    FORMAT = '\033[%dm%s'  # ANSI-start (CSI+SGR+m+sträng)
    RESET = '\033[0m'  # ANSI-slut (CSI+återställningskod+m)
    SGR = {'bold': 1, 'underline': 4, 'red': 31}  # SGR-kod
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        if attrs is not None:
            for attr in attrs:
                text = FORMAT % (SGR[attr], text)
            text += RESET
    return text


def decoprint(text: str, attrs: list = None):
    """
    Skriver ut dekorerad text i terminalfönstret.

    :param text: Textsträngen som ska dekoreras.
    :param attrs: En lista bestående av följande textelement, där
                  ingen speciell ordning på attributen i listan
                  behöver beaktas:
                        bold        - för fettstild text
                        underline   - för understruken text
                        red         - för röd text
    Exempel:
        decoprint('en text', ['bold', 'red'] - för att få röd fettstild text
    """
    print(deco(text, attrs))


def clear_terminal_screen():
    """
    Rensar terminalfönstret från text.
    """
    if platform.system() is 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def exit_system(app_name=None):
    """
    Avslutar programkörning

    :param app_name: Sträng bestående av applikationens namn.
    """
    if app_name is None:
        decoprint('Programmet har nu avslutats.', ['bold'])
    else:
        decoprint(app_name + ' har nu avslutats.', ['bold'])
    raise SystemExit


def text_user_interface(app_name: str):
    """
    Funktionen för den textbaserade användargränsnittet för programmet.

    :param app_name: Sträng bestående av applikationens namn.
    """
    print('\t' + deco(app_name, ['underline', 'bold']))
    while True:
        while True:  # Den 2:a whileloopen
            print('(1) Se kalendern för den här månaden')
            print('(2) Se kalendern för ett specifikt år och månad')
            print('(0) Avsluta')
            try:
                menu = int(input('Välj ett alternativ från menyn: '))
            except ValueError:
                decoprint('*** Du har gjort ett felaktigt val! ***', ['bold'])
                decoprint('Välj önskat menyval genom att ange dess menynummer i heltal.\n', ['bold'])
            else:
                if 0 <= menu <= 2:
                    break  # Hoppar in till den 3:e whileloopen
                else:
                    decoprint('*** Det valda menyvalet finns inte! ***', ['bold'])
                    decoprint('Det finns inget menyval som motsvaras av det givna numret "' +
                              str(menu) + '".\n', ['bold'])
        while True:  # Den 3:e whileloopen
            if menu is 2:  # Meny 2: Välj år och månad
                while True:
                    try:
                        year = int(input('Ange det år du vill titta på: '))
                    except ValueError:
                        decoprint('*** Du har anget ett felaktigt årtal! ***', ['bold'])
                        decoprint('Ange årtalet i heltal mellan (1900-3000): ' + str(Calendar.MIN_YEAR) +
                                  ' och ' + str(Calendar.MAX_YEAR) + ".\n", ['bold'])
                    else:
                        if Calendar.MIN_YEAR <= year <= Calendar.MAX_YEAR:
                            break  # Hoppar till nästa whileloop för inmatning av månad.
                        else:
                            decoprint('*** Vald år ligger utanför intervallet! ***', ['bold'])
                            decoprint('Det angivna årtalet "' + str(year) + '" är felaktigt. ' +
                                      'Årtalet måste vara\nminst ' + str(Calendar.MIN_YEAR) +
                                      ' och som högst ' + str(Calendar.MAX_YEAR) + ".\n", ['bold'])
                while True:  # Loop för inmatning av månad
                    try:
                        month = int(input('Ange numret på den månad du vill titta på (1-12): '))
                    except ValueError:
                        decoprint('*** Du har anget en felaktig månad! ***', ['bold'])
                        decoprint('Ange månaden i siffror mellan 1 och 12.\n', ['bold'])
                    else:
                        if 1 <= month <= 12:
                            clear_terminal_screen()
                            CalendarText(year, month).print_month()
                            break  # Hoppar tillbaka till den 2:a whileloopen.
                        else:
                            decoprint('*** Vald månad ligger utanför intervallet! ***', ['bold'])
                            decoprint('Den angivna månaden "' + str(month) + '" är en felaktig månad.\n' +
                                      'Ange månaden med siffror i intervallet 1-12 (jan-dec)\n' +
                                      'som motsvaras av den efterfrågade månaden.\n', ['bold'])
            elif menu is 1:  # Meny 1: Se denna månadskalender
                clear_terminal_screen()
                CalendarText(date_now=True).print_month()
            else:  # Meny 0: Avsluta
                exit_system()
            break  # Hoppar tillbaka till den 2:a whileloopen.


def main(app_name: str = 'Kalenderprogrammet'):
    """
    Huvudfunktionen för val av användningsgränssnitt.

    :param app_name: Sträng bestående av applikationens namn.
                     Som standard är namnet 'Kalenderprogrammet' förvalt.
    """
    clear_terminal_screen()
    print('\t\t' + deco(app_name, ['underline', 'bold']) + '\n')
    print('Programmet skriver ut en kalender för åren ' + str(Calendar.MIN_YEAR) +
          ' till och med ' + str(Calendar.MAX_YEAR) + '.\n')
    while True:
        decoprint('Val av gränssnitt', ['bold'])
        print('(1) Textbaserat användargränssnitt (TUI)')
        print('(2) Grafiskt användargränsnitt (GUI)')
        print('(0) Avsluta')
        try:
            menu = int(input('Välj önskat användargränsnitt: '))
        except ValueError:
            decoprint('*** Du har gjort ett felaktigt val! ***', ['bold'])
            decoprint('Välj önskat gränsnitt genom att ange dess menynummer i heltal.\n', ['bold'])
        else:
            if menu is 1:
                clear_terminal_screen()
                text_user_interface(app_name)
            elif menu is 2:
                root = Tk()
                Application(root, app_name)
                root.mainloop()
                exit_system(app_name)
            elif menu is 0:
                exit_system(app_name)
            else:
                decoprint('*** Det valda menyvalet finns inte! ***', ['bold'])
                decoprint('Det finns inget gränssnitt som motsvarar\ndet efterfrågade ' +
                          'menyvalet: "' + str(menu) + '".\n', ['bold'])


if __name__ == '__main__':
    main()
