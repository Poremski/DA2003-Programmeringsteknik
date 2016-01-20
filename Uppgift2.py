# Programmeringsteknik webbkurs KTH inlämningsuppgift 2.
# Andreas Poremski
# 2014-10-30
# Genererering av dikt utifrån fyra meningar.

sentence = 4*[None]

# Delar upp orden efter mallen för hur dikten ska se ut.
# 'Nbr' är nummerelementet för listvariabeln 'sentence'.
# 'Type' = 1 => returnerar de första fyra elementen i sentence[nbr]
# 'Type' = 2 => returnerar alla element i sentence[nbr], bortsett från de fyra första.
# Else => returnerar samtliga element.
def getWords(nbr, type):
    if type == 1:
        return " ".join(sentence[nbr][:4])
    elif type == 2:
        return " ".join(sentence[nbr][4:len(sentence[nbr])])
    else:
        return " ".join(sentence[nbr])

# Hämtar in fyra meningar.
def getSentences():
    for x in range (0, 4):
        sentence[x] = input("Skriv mening nr " + str(x+1) + ": ").split()

# Skriver ut programmets titel
def headTitle():
    print("""\t\tDIKTAUTOMATEN\n
Skriv in fyra meningar och få ut en rondelet!\n""")

# Returnerar diktens titel
def printTitle():
    return getWords(0,1).upper()

# Skriver ut dikten och dess titel
def printPoem():
    print("")
    print("")
    print(printTitle())
    print("")
    print(getWords(0,1))
    print(getWords(0,2))
    print(getWords(0,1))
    print(getWords(1,0))
    print(getWords(2,0))
    print(getWords(3,0))
    print(getWords(0,1))

def start():
    headTitle()    # Huvudtiteln på programmet
    getSentences() # Hämtar in meningarna
    printPoem()    # Skriver ut dikten
    
start()
