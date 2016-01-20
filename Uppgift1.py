# Programmeringsteknik webbkurs KTH inlämningsuppgift 1.
# Andreas Poremski
# 2014-10-22
# Ett fyrsiffrigt tal matas in och antalet iterationer beräknas 
# för att uppnå Kaprekars konstant (6174). 

# Start av kontroll av inmatning
condition = True
while condition:
    inData = input("Ante ett fyrsiffrigt tal: ")
    if str.isdigit(inData) == False:
        print("Ange ett heltal.")
    elif len(inData) < 4:
        print("Talet är för litet.")
    elif len(inData) > 4:
        print("Talet är för stort.")
    else:
        countNbr = 0
        for i in range(4):
            if inData[0] == inData[i]:
                countNbr += 1
        if countNbr != 4:
            condition = False
        else:
            print("Talet får ej bestå av fyra likadana siffror i följd.")
# Slut på kontroll

tmp = inData
count = 0

# Start av uträkning
while True:
    if tmp == "6174":
        break
    large = "".join(sorted(tmp, reverse=True))
    small = "".join(sorted(tmp, reverse=False))
    # Säkerställer att variabeln 'large' består av 4 tecken.
    while len(large) < 4:
        large += "0"
    tmp = str(int(large) - int(small))
    count += 1
# Slut på uträkning

print("Det tog", count, "interationer att nå " + tmp + ".")
