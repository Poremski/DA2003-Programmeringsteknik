# -*- coding: utf-8 -*-

# Programmeringsteknik webbkurs KTH inlämningsuppgift 3.
# Andreas Poremski
# 2016-01-20
# Ett program som simulerar ett nöjesfält.

import math
import random

REACTIONS = ["Snark!", "Zzzz!", "Mmm…", "Yahoo!", "Wiii!", "Waaa!", "Iiiih!", "WAAAA!", "Aaaa!", "AAAA!"]
QUALITY = 5; # Sannolikheten för attraktionen att haverera är 1/QUALITY. 

# Returnerar strängen 'msg' med en ram bestående av tacknet 'char'.
class GraphicBox:
    def __init__(self):
        self.char = None
        self.msg = None
    
    # Kind 1 - rubrik (med texten 'msg', radbyte, och teckenrad 'char')
    # Kind 2 - kvadrat (med texten 'msg' inramad med tecknet 'char')
    def drow(self, char, msg, kind):
        self.char = str(char)
        if kind == 1:
            self.msg = " " + str(msg) + " \n"
            self.msg += self.char*(len(str(msg))+2)
        elif kind == 2:
            tmp = msg.split("\n")
            # Om strängen består av radbyte.
            if int(len(tmp)) > 1:
                maxLength = 0
                # Räknar ut den längsta raden på textsträngen
                for x in range(len(tmp)):
                    if maxLength < len(tmp[x]):
                        maxLength = len(tmp[x])
                self.msg = self.char*(maxLength+4) + "\n"
                # Tilldelar ramen till textsträngen
                for x in range(len(tmp)):
                    self.msg += self.char + " " + str(tmp[x]) + " "*(maxLength-int(len(tmp[x]))+1) + self.char + "\n"
                self.msg += self.char*(maxLength+4) + "\n"
            # Textsträngen är utan radbyte
            else:
                self.msg = self.char*(len(str(msg))+4) + "\n"
                self.msg += self.char + " " + str(msg) + " " + self.char + "\n"
                self.msg += self.char*(len(str(msg))+4)
        else:
            try:
                raise ValueError("*** Error: Oförväntad värde i variablen 'kind' i metoden GraphicBox.drow()! ***")
            except ValueError as e:
                print(e)
                
        return self.msg

# Innehåller information om besökaren
class Visitor:
    def __init__(self):
        self.visitors = []
    
    # Lägger till besökare
    def add(self, name, height):
        self.visitors.append([name, height])
    
    def __iter__(self):
        return iter(self.visitors)

# Innehåller information om attraktionen     
class Ride:
    def __init__(self, name, minHeight, thrill):
        self.name = name
        self.minHeight = minHeight
        self.thrill = thrill
        self.broken = False
        self.queue = []
    
    # Lägger in besökaren i kö
    def addToQueue(self, visitor):
        if self.minHeight > visitor[1]:
            print("--> " + str(visitor[0]) + ": Du måste vara minst " + str(self.minHeight) + " cm lång, för att åka", str(self.name) + ".")
        else:
            self.queue.append(visitor)
            print("-->", str(visitor[0]) + ": Du står nu i kö till", self.name + ".")

    # Attraktionen startar
    def start(self):
        if len(self.queue) != 0:
            print("3… 2… 1… – Nu startar", self.name + "! – och nu var åkturen över. Tack för besöket!")
            if not math.floor(random.random()*QUALITY):
                print("Tekniska problem!", self.name, "är ur funktion.")
                self.broken = True
            else:
                # En körning per besökare
                for x in range(len(self.queue)):
                    tmp = self.queue.pop()
                    scariness = math.floor(random.random()*self.thrill)
                    reaction = REACTIONS[scariness]
                    print(tmp[0] + ":", reaction)
    
    def __iter__(self):
        return self
# Nöjesparken
class AmusementPark:
    def __init__(self, name):
        self.name = name
        self.rides = []
    
    # Returnerar lista med attraktionerna
    def __iter__(self):
        return iter(self.rides)
    
    # Returnerar antalet attraktioner
    def __len__(self):
        return len(self.rides)
    
    # Lägger till möjlighet för indexering vid menyval
    def __getitem__(self, index):
        return self.rides[index-1]
    
    # Lägger till en ny attraktion
    def addRide(self, name, minHeight, thrill):
        self.rides.append(Ride(name, minHeight, thrill))
      
# Huvudprogrammet
class main():
    box = GraphicBox()
    guest = Visitor()
    park = AmusementPark("The Fun Park")
    
    park.addRide("The Psychedelic Insanity", 160, 9)
    park.addRide("The Magic Mountain", 140, 6)
    park.addRide("The Tea Cups", 120, 2)
    
    # Rubriken
    print(box.drow("=", "Välkommen till %s!" % park.name, 1))

    # Input: antal besökare
    while True:
        try:
            n = int(input("Hur många besökare är ni? "))
            if isinstance(n, int):
                break
        except ValueError:
            print(box.drow("*", "Ange antalet besökare med siffror.", 2))
            
    # Input: besökarens namn
    while True:
        for i in range(n):
            while True:
                name = str(input("Ange namnet på besökaren nr. %i: " % (i+1)))
                if len(name) > 0:
                    break
                else:
                    print(box.drow("*", "Ett namn på besökaren måste anges.", 2))
            
            # Input: besökarens längd
            while True:
                try:
                    height = int(input("Ange längden på besökaren %s i centimeter: " % name))
                    if isinstance(height, int):
                        guest.add(name, height)
                        break
                except ValueError:
                    print(box.drow("*", "Längden ska anges i centimeter.", 2))
        break
    
    while True:
        # Inne i parken
        menuNbr = 1
        goToMenu = False
        exit = False
        while True:
            # Output: Meny-listan över attraktioner
            print("\n" + box.drow("=", "Attraktioner", 1))
            for ride in park:
                if ride.broken:
                    print(" " + str(menuNbr) + ":", ride.name, "– (Ej i drift)")
                else:
                    print(" " + str(menuNbr) + ":", ride.name, "– (Magpirrfaktor:", ride.thrill, ")")
                    
                menuNbr += 1
            
            print(box.drow("-", "0: Lämna " + park.name, 1))
        
            # Kontroll av att användarens input av menyval är korrekt.
            try:
                n = int(input("Välj (0-" + str(menuNbr-1) + "): "))
                if isinstance(n, int):
                    print(len(park))
                    if (n > len(park)) or n < 0:
                        print(box.drow("*", "Meny nr. " + str(n) + " finns inte!", 2))
                        pause = input("Tryck valfri tagent för att återgå till menyn.")
                    else:
                        while True:
                            if n == 0:
                                print(box.drow("*", "Hej då", 2))
                                goToMenu = True
                                exit = True
                                break
                            elif park[n].broken:
                                print("\n" + box.drow("*", park[n].name + " är stängd för underhållsarbete.", 2))
                                pause = input("Tryck valfri tagent för att återgå till menyn.")
                                goToMenu = True
                                break
                            elif not park[n].broken:
                                for v in guest:
                                    park[n].addToQueue(v)
                                park[n].start()
                                pause = input("Tryck valfri tagent för att återgå till menyn.")
                                goToMenu = True
                                break
                            else:
                                print("\n" + box.drow("*", "Du måste välja nåt ur menyn.", 2))
                                pause = input("Tryck valfri tagent för att återgå till menyn.")
                                goToMenu = True
                                break
                                
            except ValueError:
                print(box.drow("*", "Felaktigt menyval – försök igen.", 2))
                pause = input("Tryck valfri tagent för att återgå till menyn.")
                
            menuNbr = 1 # Återställer menynumreringen
            
            # Hoppar tillbaka in i menyn
            if (goToMenu):
                break
        # Programmet avslutas
        if (exit):
            break

 
main()
print("Programmet har nu avslutats.")
