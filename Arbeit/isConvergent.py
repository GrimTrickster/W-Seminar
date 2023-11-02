from sympy import Symbol, sympify, zoo, Derivative, solve
import matplotlib.pyplot as plt
import numpy as np

x = Symbol('x')


def funktionZuFolge(funktion, max_length):
    a = []
    max_problemstelle = None
    for i in range(max_length):
        y = funktion.subs(x, i)
        if y == zoo:
            max_problemstelle = i
            a.append(None)
        else:
            a.append(y.evalf())
    return a, max_problemstelle


# ############### Get User Input #####################
#   Get+Create Function
userInputFunktion = input('Bitte geben Sie eine zu überprüfende Funktion mit der Variable x an.')
if userInputFunktion == '':
    userInputFunktion = 'x/(x+1)+2'

print('=>  ' + userInputFunktion)
f = sympify(userInputFunktion)


#   Get Max Iterations
userInputMaxIterations = input('Bitte geben Sie die maximale Anzahl der zu überprüfenden Folgenglieder an.')
if userInputMaxIterations == '':
    userInputMaxIterations = 1000
else:
    userInputMaxIterations = int(userInputMaxIterations)
print('=>  ' + str(userInputMaxIterations))


# #################### Erstelle Folge ###################################

folge, maxProblemstelle = funktionZuFolge(f, userInputMaxIterations)
print(folge)
print("Problemstellen: " + str(maxProblemstelle))

# ####################### Startindex ermitteln ######################
startIndex = 0
f_erste_ableitung = Derivative(f, x).doit()
problemstellen = solve(f_erste_ableitung)

if maxProblemstelle is not None:
    problemstellen.append(maxProblemstelle)
print(problemstellen)

if len(problemstellen) > 0:
    startIndex = 1
    #startIndex = max(problemstellen) + 1
print(startIndex)
# TODO: Nullstellen überprüfen


# ############################## Grenzwert bestimmen######################################

# Startvariablen festlegen (Start bei 1, da vorherige Werte benötigt werden)
prevValue = folge[0 + startIndex]
currValue = folge[1 + startIndex]
currDiff = 0
prevDiff = 0
grenzwert = None

# Über alle Folenglieder iterieren
for i in range(2+startIndex, userInputMaxIterations):
    # Betrag um Annäherung von unten und von oben zu berücksichtigen
    currDiff = abs(currValue - prevValue)

    if currDiff > prevDiff and i != 2+startIndex:
        grenzwert = None
        break

    grenzwert = currValue
    prevValue = currValue
    currValue = folge[i]
    prevDiff = currDiff


plt.plot(range(0, userInputMaxIterations), folge, 'ro')
if grenzwert:
    print('Grenzwert: ' + str(grenzwert.evalf()))
    plt.axhline(y=grenzwert, color='r', linestyle='-')
plt.show()
