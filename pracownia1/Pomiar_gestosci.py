#!/usr/bin/env python2
#-*- coding: utf-8 -*-

__author__ = 'Pawel Chojnacki'
__copyright__ ='Copyleft 2013 Pawel Chojnacki'
__version__ = '2.0'
__date__ = '29-03-2013'
__license__ = 'GPLv3'

import numpy as np
import matplotlib as mpl # Zmiana ustawien LaTeXa
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}']
mpl.rcParams['text.latex.unicode'] = True
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
import pylab as py

class pomiary(object):

	def __init__(self,lista,delta=0):
		self.wyn = lista
		self.delta = delta	# Niepewnosc pomiaru (najmniejsza podzialka)

	def __str__(self):
		return str("Dla pomiarow "+str(self.wyn)+"\nStandardowe Odchylenie Probki wynosi "\
		+str(self.sop)+"\nStandardowe Odchylenie Sredniej wynosi "+str(self.sos))
		
	def __add__(a,b):
		return S1.wyn + S2.wyn
		
	def srednia(self):
		return np.mean(self.wyn)
		
	def mediana(self):
		return np.median(self.wyn)
	
	def sopomiaru(self):
		return np.std(self.wyn,ddof=1) # CHOLERNIE CHOLERA WAZNE
		# TO JEST TAKIE WAZNE, ZE TRZEBA MU POSWIECIC AZ KILKA LINIJEK
		# DDOF O ZNACZA, O JAKA LICZBE MA BYC POMNIEJSZONY N PRZY DZIELENIU
		# DLA ROZKLADOW NIEPELNEJ POPULACJI MA BYC N-1, JASNE? J A S N E?
		# bo ja nie wiedzialem. domyslnie = 0.

	def sosredniej(self):
		return self.sopomiaru() / len(self.wyn)**0.5
		
	def blad_pomiaru(self):
		return np.sqrt(self.sopomiaru()**2 + (1./3)*self.delta**2)
		
	def blad_sredniej(self):
		return np.sqrt(self.sosredniej()**2 + (1./3)*self.delta**2)


### DANE ###

S1 = pomiary((24.04, 24.04, 24.03, 24.03, 23.97, 23.97, 23.97, 23.99, 23.98, 23.99),0.01)
S2 = pomiary((23.99, 24.01, 23.97, 23.98, 23.97, 23.98, 23.98, 23.99, 23.98, 24.00),0.01)
h1 = pomiary((39.60, 39.58, 39.60, 39.60, 39.62, 39.62, 39.59, 39.60, 39.58, 39.61),0.01)
m1 = pomiary((149.83,149.83,149.83,149.83,149.83,148.83,149.83,149.83,149.82,149.82),0.01)
S3 = pomiary(S1 + S2) # Albo podstaw tu sobie wlasne pomiary srednicy
V1 = (50.2 - 33) # W przypadku pomiaru jednokrotnego, delta = 0.2 cm^3
Ro_w = 997.0960 # Gestosc wody z P.H. Bigg, Brit. J. Appl. Phys. 18, 521 (1967).
N1 = pomiary((17.74, 17.74, 17.73, 17.74, 17.73),0.01) # Mierzylem tylko roznice pomiarow

### PROGRAM ###u

# POMIARY BEZPOSREDNIE
# u^2 = s^2 + 1/3 delta^2
D = S3.srednia() / 1000 # Milimetry -> Metry
H = h1.srednia() / 1000 # Milimetry -> Metry
M = m1.srednia() / 1000 # Gramy -> Kilogramy
V = V1 / 1E6 # cm^3 -> m^3
N = N1.srednia() / 1000 # Gramy -> Kilogramy
# NIEPEWNOSCI BEZWZGLEDNE
Db = S3.blad_sredniej()/1000 # Milimetry -> Metry
Hb = h1.blad_sredniej()/1000 # Milimetry -> Metry
Mb = m1.blad_sredniej()/1000 # Gramy -> Kilogramy
Vb = 0.2/1E6 # Mnozenie, poniewaz odejmujemy od siebie dwie wartosci 
Nb = N1.blad_sredniej()/1000 # Gramy -> Kilogramy
# NIEPEWNOSCI WZGLEDNE
Dw = Db/D
Hw = Hb/H
Mw = Mb/M
Vw = Vb/V
Nw = Nb/N

#~ print Db*1000,Hb*1000,Mb*1000 # Wartosci w mm/mg
print Dw,Hw,Mw,Vw,Nw

# METODA A
Ro_A = 4*M / (np.pi*D**2*H)	# Wartosc gestosci
Ro_A_w = np.sqrt( Mw**2 + (2*Dw)**2 + Hw**2 ) # Niepewnosc wzgledna
Ro_A_b = Ro_A * Ro_A_w # Niepewnosc bezwzgledna, nie zna litosci
print round(Ro_A,2), Ro_A_w, round(Ro_A_b,2)

# METODA B
Ro_B = M / V
Ro_B_w = np.sqrt( Mw**2 + 2*Vw**2 ) # Dwa razy, bo odejmujemy
Ro_B_b = Ro_B * Ro_B_w
print round(Ro_B,2), Ro_B_w, round(Ro_B_b,2)

# METODA C
Ro_C = (M * Ro_w) / N
Ro_C_w = np.sqrt( Mw**2 + 2*Nw**2 ) # Dwa razy, bo odejmujemy
Ro_C_b = Ro_C * Ro_C_w
print round(Ro_C,2), Ro_C_w, round(Ro_C_b,2)

# YAY RYSUJEMY WYYYYYKREEEEES YAY YAY YAY
# Zadne tam wykresy, potrzebujemy errorbara

x = range(1,4)
y = [ Ro_A, Ro_B, Ro_C ]
yerr = [ Ro_A_b, Ro_B_b, Ro_C_b ]

fig = py.figure()
ax = fig.add_subplot(111)
py.errorbar(x,y,yerr=yerr,fmt='ko',elinewidth=1,capsize=5)
py.axhspan(8400,8730,alpha=0.15)
for i in range(1,4):
	a,b = i,y[i-1]
	ax.text(a,b,str(int(b)),withdash=True,dashdirection=1,dashlength=10,dashpush=10)
py.title(u'Wyniki eksperymentu pomiaru gęstości ciała stałego',size='x-large')
py.ylabel(u'Gęstość ciała stałego ' + r'$\left[\frac{\text{kg}}{\text{m}^3}\right]$',size='large')
py.xlabel(r'Metoda pomiaru',size='large')
py.yticks(size='large')
py.xticks(range(1,4),('A','B','C'),size='large')
py.xlim(min(x)-0.5,max(x)+0.5) # Linijka dla marginesow
py.grid(True)
py.show()
