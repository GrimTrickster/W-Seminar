from sympy import Symbol, sympify, zoo, diff, S, pprint, solveset
import matplotlib.pyplot as plt
from math import ceil

# Sympy-Schreibweise um x als Variable zu definieren
x = Symbol('x')


def funktionZuFolge(funktion, max_length):
    a = []
    max_problemstelle = None
    for i in range(max_length):
        # Sympy: Wert der Funktion an einer gewissen Stelle ausrechnen; "x mit einer entsprechenden Zahl SUBstituieren
        y = funktion.subs(x, i)
        # Definitionslücken auffinden
        if y == zoo:
            max_problemstelle = i
            a.append(None)
        else:
            a.append(y.evalf())
    return a, max_problemstelle


# ############### Get User Input #####################
#   Get+Create Function
userInputFunktion = input('Bitte geben Sie eine zu überprüfende Funktion mit der Variable x an.')
# Standard-Option wenn nichts eingegeben wird
if userInputFunktion == '':
    userInputFunktion = 'x/(x+1)+2'

f = sympify(userInputFunktion)
pprint(f)

#   Get Max Iterations
userInputMaxIterations = input('Bitte geben Sie die maximale Anzahl der zu überprüfenden Folgenglieder an.')
# Standard-Option wenn nichts eingegeben wird
if userInputMaxIterations == '':
    userInputMaxIterations = 1000
else:
    userInputMaxIterations = int(userInputMaxIterations)
print('=>  ' + str(userInputMaxIterations))


# #################### Erstelle Folge ###################################

folge, maxProblemstelle = funktionZuFolge(f, userInputMaxIterations)
print(folge)

# ####################### Startindex ermitteln ######################
startIndex = 0
f_erste_ableitung = diff(f, x)
problemstellenSet = solveset(f_erste_ableitung, x, domain=S.Reals)
problemstellen = []
for solution in problemstellenSet.args:
    problemstellen.append(solution.evalf())

if maxProblemstelle is not None:
    problemstellen.append(maxProblemstelle)
print('Problemstellen: ' + str(problemstellen))

if len(problemstellen) > 0:
    if max(problemstellen) == ceil(max(problemstellen)):
        startIndex = ceil(max(problemstellen)) + 1
    else:
        startIndex = ceil(max(problemstellen))
print('Startindex: ' + str(startIndex))


# ############################## Grenzwert bestimmen######################################

# Startvariablen festlegen (Start bei 1, da vorherige Werte benötigt werden)
prevWert = folge[0 + startIndex]
currWert = folge[1 + startIndex]
currDiff = 0
prevDiff = 0
grenzwert = None

# Über alle Folenglieder iterieren
for i in range(2+startIndex, len(folge)):
    # Betrag um Annäherung von unten und von oben zu berücksichtigen
    currDiff = abs(currWert - prevWert)

    if currDiff > prevDiff and i != 2+startIndex:
        grenzwert = None
        break

    grenzwert = currWert
    prevWert = currWert
    currWert = folge[i]
    prevDiff = currDiff


plt.plot(range(0, userInputMaxIterations), folge, 'ro', markersize=3)
if grenzwert:
    print('Grenzwert: ' + str(grenzwert.evalf()))
    plt.axhline(y=grenzwert, color='b', linestyle='-')
plt.show()
