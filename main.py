import cv2
import pydicom
import numpy as np
import re

dataset = pydicom.dcmread("IM_0093.dcm")
# imie nazwisko wiek waga rodzaj badania data wykonania badania ciąża
# print(dataset.PatientName)
try: 
    print("Name: " + dataset[(0x0010, 0x0010)].value)  # imie nazwisko
except: pass
try: 
    x = dataset[(0x0010, 0x1010)].value  # wiek
    s = ''.join(filter(str.isdigit, x))
    s = int(s)
except: pass
print("Age: " + str(s))
try: print("Weight: " + str(dataset[(0x0010, 0x1030)].value))  # waga
except: pass
try: print("Study description: " + dataset[(0x0008, 0x1030)].value)  # rodzaj badania
except: pass
try: print("Study date: " + dataset[(0x0008, 0x0020)].value)  # data wykonania
except: pass
try: 
    x = dataset[(0x0010, 0x21C0)].value  # ciąża
    if x == 1: print("Pregnancy status: not pregnant")
    if x == 2: print("Pregnancy status: possibly pregnant")
    if x == 3: print("Pregnancy status: definitely pregnant")
    if x == 4: print("Pregnancy status: unknown")

except: pass

wspolrzedne_nacisn = 0


def klikniecie(event, x, y, flags, param):
    global wspolrzedne_nacisn
    if event == cv2.EVENT_LBUTTONDOWN:
        wspolrzedne_nacisn = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        wspolrzedne_puszczone = (x, y)
        print("Klawisz nacisniety we wspolrzednych {}, puszczony we wspolrzednych {}".format(wspolrzedne_nacisn, wspolrzedne_puszczone))


obraz = dataset.pixel_array
print(type(obraz[0, 0]))
print(dataset.BitsAllocated)

wart_min = np.amin(obraz)
wart_max = np.amax(obraz)
obraz = (obraz - wart_min)*255.0/wart_max
cv2.imwrite('plik1.png', obraz)

obrazek = cv2.imread('plik1.png')
cv2.imshow('Obrazek do klikania',obrazek)
cv2.setMouseCallback("Obrazek do klikania", klikniecie)

k = cv2.waitKey(0)
print("Nacisnieto klawisz: {}".format(k))
cv2.destroyAllWindows()