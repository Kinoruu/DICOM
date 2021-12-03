import cv2
import pydicom
import numpy as np
import re
import math

dataset = pydicom.dcmread("IM_0093.dcm")
# Proszę przygotować program, który wczyta podany mu w linii poleceń plik DICOM, Wypisze
# podstawowe informacje o pliku w konsoli: imię i nazwisko pacjenta, wiek, waga, rodzaj badania
# (0x0008,0x0060) oraz inne informacje, jeśli występują – data wykonania sesji badania, czy jest w
# ciąży (przydatna może być pythonowa konstrukcja try, except).

try: 
    print("Name: " + dataset[(0x0010, 0x0010)].value)  # imie nazwisko
except:
    print("Name: Unknown")
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

# Następnie program wyświetli obraz na ekranie i pozwoli na dokonanie pomiarów odległości między
# różnymi punktami obrazu zaznaczanymi myszą. Konieczne okaże się tu wykorzystanie pola
# PixelSpacing, w którym zawarta jest informacja o odstępie w milimetrach między kolejnymi
# punktami obrazu

wspolrzedne_nacisn = 0
wspolrzedne_puszczone = 0

# pixel_spaing
psy, psx= dataset[(0x0028, 0x0030)].value

def klikniecie(event, x, y, flags, param):
    global wspolrzedne_nacisn
    global wspolrzedne_puszczone
    global xn, yn, xp, yp
    if event == cv2.EVENT_LBUTTONDOWN:
        # wspolrzedne_nacisn = (x, y)
        xn = x
        yn = y
    elif event == cv2.EVENT_LBUTTONUP:
        # wspolrzedne_puszczone = (x, y)
        xp = x
        yp = y
        # print("Klawisz nacisniety we wspolrzednych {}, puszczony we wspolrzednych {}".format(wspolrzedne_nacisn, wspolrzedne_puszczone))
        # c = math.sqrt(pow(abs(wspolrzedne_nacisn.index(0) - wspolrzedne_puszczone.index(0)), 2) +
                      # pow(abs(wspolrzedne_nacisn.index(1) - wspolrzedne_puszczone.index(1)), 2))
        c = math.sqrt(pow(abs(xn - xp) * psx, 2) + pow(abs(yn - yp) * psy, 2))
        print(str(round(c, 2)) + 'mm')


obraz = dataset.pixel_array

wart_min = np.amin(obraz)
wart_max = np.amax(obraz)
obraz = (obraz - wart_min)*255.0/wart_max
cv2.imwrite('plik1.png', obraz)

obrazek = cv2.imread('plik1.png')
cv2.imshow('Obrazek do klikania',obrazek)
cv2.setMouseCallback("Obrazek do klikania", klikniecie)

k = cv2.waitKey(0)
# print("Nacisnieto klawisz: {}".format(k))
cv2.destroyAllWindows()
