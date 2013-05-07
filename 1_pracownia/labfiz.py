#!/usr/bin/env python2

__author__ = 'Pawel "duskglow" Chojnacki'
__copyright__ ='Copyleft 2013 Pawel Chojnacki'
__version__ = '0.8'
__date__ = '07.05.2013'
__license__ = 'GPLv3'

import numpy as np
# Dzieki ponizszym linijkom caly tekst generowany bedzie w LaTeXu
# co pozwoli na uzycie np. r'$\frac{1}{2}$'
import matplotlib as mpl
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}']
mpl.rcParams['text.latex.unicode'] = True
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
import pylab as py

class pomiary(object):
	'''Klasa pomiarow zawierajaca pomiary fizyczne i odpowiadajacy im blad pomiaru, pozwala na podstawowe operacje na danych z pracowni fizycznej.'''
	def __init__(self,lista,delta=0): # Wolamy ja pomiary((lista wartosci),delta)
		self.w = np.array(lista)
		self.d = delta	# Niepewnosc pomiaru (najmniejsza podzialka)

	def __str__(self): # Aby wypisywal wartosci i delte 
		return str(self.w),str(self.d)

	def __add__(self,b): # Dodawanie dwoch zbiorow pomiarow lub liczby
		if type(b) == pomiary:
			if self.d != b.d: # Wywali blad, kiedy dodajemy pomiary o roznych deltach
				raise Exception('Rozne bledy pomiarow!')
			else:
				return pomiary(np.append(self.w,b.wyn), self.d)
		elif type(b) in (int,float): # dodaje wartosc do wszystkich wartosci pomiarow
			return pomiary(self.w + b,self.d)
		else:
			raise Exception('Wspierane mnozenie przez liczbe lub pomiary!')
		
	def __mul__(self,b): # Mnozenie pomiarow razy liczba
		if type(b) in (int,float):
			return pomiary(self.w*b,self.d*b) # mnozymy zarowno pomiary, jak i delte
		else:
			raise Exception('b powinno byc liczba!')
		
	def sr(self): # Srednia
		return np.mean(self.w)
		
	def med(self): # Mediana
		return np.median(self.w)
	
	def war(self): # Wariancja
		return np.var(self.w)
	
	def sop(self): # Srednie odchylenie pomiaru, ddof=1 == N(N-1)
		return np.std(self.w,ddof=1)

	def sos(self): # Srednie odchylenie sredniej
		return self.sop() / len(self.w)**0.5
		
	def np(self): # Niepewnosc pomiaru
		return np.sqrt(self.sop()**2 + (1./3)*self.d**2)
		
	def ns(self): # Niepewnosc sredniej
		return np.sqrt(self.sos()**2 + (1./3)*self.d**2)
		
	def hist(self,przedz=0,krok=1,norm=0,wys=0,osX=0,osY=0,sr=0,sig=0,tyt=0):
		histogram(self.w,przedz,krok,norm,wys,osX,osY,sr,sig,tyt)
		
	def whist(self,serie,przedz=0,krok=1,norm=0,wys=0,osX=0,osY=0,sr=0,sig=0,tyt=0):
		dane = self.w
		

def histogram(dane,przedz=0,krok=1,norm=0,sig=0,sr=0,dop=0,wys=0,osX=0,osY=0,tyt=0,fs='x-large'):
	'''Rysuje histogram nie wyswietlajac go - potrzeba zakonczyc py.show().
	dane - wektor danych (krotka/lista/array)
	przedz - przedzial do narysowania (lista/array)
	krok - krok histogramowania (int/float)
	norm - normalizowac? 'g'estosc / 'c'zestosc / False
	sig  - rysowac zakresy ilu sigm? (int/float)
	sr - pokazac srednia? (True/False)
	dop - dopasuj funkcje - 0/'gauss' - dziala przy norm=0 lub 'g'
	wys - wysokosc histogramu, 0 - policzy sam (int/float)
	osX - podpis osi X (str)
	osY - podpis osi Y (str)
	tyt - tytul (str)
	fs - fontsize (str/int)'''
	if not bool(przedz): przedz = np.arange(min(dane),max(dane)+krok,krok) # Jezeli przedzialy nie istnieja, generuje sam
	if norm=='c': wagi = [1./len(dane)] * len(dane) # Jezeli normuje wg czestosci, liczy wagi (moglby tez mnozyc gestosci, ale to kiedy indziej) 
	else: wagi = [1.]*len(dane)
	if norm=='g': gest = True
	else: gest = False
	if wys!=0: py.ylim((0,wys)) # Ustawia wysokosc, jezeli istnieje
	py.xlim((min(dane)-krok/2,max(dane)+krok/2)) # Ogranicza X do min i max wartosci + pol kroku
	py.hist(dane,bins=przedz,weights=wagi,normed=gest,color='gray') # Rysowanie histogramu
	py.xticks(rotation=45,size=fs) # wielkosc czcionki, wartosci pod katem
	py.yticks(size=fs) # tylko wielkosc czcionki
	if sr!=0: py.axvline(np.mean(dane),color='black') # srednia
	if sig!=0: #przedzialy ufnosci
		sigma = sig*np.std(dane) # szerokosc (sig) sigm
		msig,Msig = np.mean(dane)-sigma,np.mean(dane)+sigma # skad dokad sigmy
		py.axvspan(msig,Msig,alpha=.25) # rysowanie spanu
		procent = sum(map(lambda d: msig < d <= Msig,dane)) / float(len(dane)) #automatycznie liczy, ile procent danych znajduje sie w przedziale
		print "W przedziale", sigma, "znajduje sie", procent
	py.grid(True) # rysuje siatke
	if tyt!=0: py.title(tyt,family='serif',size=fs) # ustawia tytul, jezeli istnieje
	if osX!=0: py.xlabel(osX,family='serif',size=fs)
	if osY!=0: py.ylabel(osY,family='serif',size=fs)
	if dop=='gauss': #dopasowuje gaussa
		from scipy.stats import norm
		wek = norm.fit(dane) # wek wynosi [miu,sigma] ze wzoru dopasowania
		osG = np.linspace(py.xlim()[0],py.xlim()[1],100) # generuje nowa gestsza os X, na ktorej narysuje gaussa
		fit = norm.pdf(osG,loc=wek[0],scale=wek[1]) # tworzy os Y gaussa
		py.plot(osG,fit*((krok*len(dane))**(1-gest)),color='black') # i w koncu go rysuje
		
def whist(dane,przedz=0,krok=1,norm=0,sig=0,sr=0,dop=0,wys=0,osX=0,osY=0,tyt=0,fs='x-large'):
	'''Rysuje wiele histogramow w oknach identycznych z pierwszym
	dane - wektor list danych (krotka krotek/lista list/array arrayow)
	przedz - przedzial do narysowania (lista/array)
	krok - krok histogramowania (int/float)
	norm - normalizowac? 'g'estosc / 'c'zestosc / Fa,se
	sig  - rysowac zakresy ilu sigm? (int/float)
	sr - pokazac srednia? (True/False)
	dop - dopasuj funkcje - 0/'gauss' - dziala przy norm=0 lub 'g'
	wys - wysokosc histogramu, 0 - policzy sam (int/float)
	osX - podpis osi X (str)
	osY - podpis osi Y (str)
	tyt - tytul (str/lista stringow)
	fs - fontsize (str/int)'''
	# Przygotowanie identyncznych przedzialow
	if przedz==0: # Stworzenie przedzialow
		mini = min(min(dane[j]) for j in range(len(dane)))
		maks = max(max(dane[j]) for j in range(len(dane)))
		if krok == 0: krok = 1
		p = list(np.arange(mini,maks,krok))
	if wys==0: # Liczenie wysokosci wszystkich wykresow
		wys = max( max(np.histogram(dane[i],bins=p,weights=wagi[i])[0]) for i in range(len(dane)) )
		wys = wys * 1.05 # piec procent wieksze, tak dla czytelnosci
	for i in range(len(dane)):
		py.figure(i)
		if tyt and type(tyt) in [list,list]: # Jezeli kazdy hist ma miec inny tytul, okej
			self.hist(dane[i],przedz,krok,norm,sig,sr,dop,wys,osX,osY,tyt[i],fs)
		else: # Albo wszystkie beda mialy takie same
			self.hist(dane[i],przedz,krok,norm,sig,sr,dop,wys,osX,osY,tyt,fs)
			
def dop_lin(x,y,nx=0,ny=0,osX=0,osY=0,podp=0,r=3,ts='large'):
	'''Rysuje dane i dopasowuje do nich linie prosta. Wymaga py.show()
	x - wartosci x, tuple/list/array - i tak zmieni sie na liste
	y - wartosci y, tuple/list/array
	nx,ny - niepewnosci x,y (tuple/list/array o dlugosci rownej powyzszym)
	osX - podpis osi X, str
	osY - podpis osi Y, str
	podp - czy podpisywac? 1,2,3,4, polozenie od lewego gornego wg wskazowek zegara
	r - zaokraglenie wartosci w podpisach, ilosc miejsc po przecinku
	ts - textsize'''
	py.errorbar(x,y,xerr=nx,yerr=ny,fmt='k.') # rysuje errorbary, czyli wartosci z przedzialami ufnosci dla kazdej
	AxB = np.polyfit(x,y,1) # dopasowuje parametry prostej (wielomianu zerowego stopnia)
	xlim,ylim = py.xlim(),py.ylim() # pobiera obecne max i min wartosci wyswietlanych X i Y
	dopx = [xlim[0]] + list(x) + [xlim[1]] # przedluza wartosci X do liczenia linii, zeby wydawala sie ciagla
	dopy = [ i*AxB[0] + AxB[1] for i in dopx] # oblicza wartosc Y dla kazdego X linii
	py.ylim(ylim) # Upewnia sie, ze os Y sie nie zmienila
	py.plot(dopx,dopy,color='k') # plotuje linie
	if osX!=0: py.xlabel(osX,family='serif',size=ts) # podpis osi X
	if osY!=0: py.ylabel(osY,family='serif',size=ts) # podpis osi Y
	if podp!=0: # jezeli ma podpisywac
		if podp in [1,4]: xP = xlim[0]+0.05*(xlim[1]-xlim[0]) # wybiera w ktorym rogu
		if podp in [2,3]: xP = xlim[1]-0.45*(xlim[1]-xlim[0])
		if podp in [1,2]: yP = ylim[1]-0.1*(ylim[1]-ylim[0])
		if podp in [3,4]: yP = ylim[0]+0.1*(ylim[1]-ylim[0])
		wektstr = 'A + Bx = '+str(round(AxB[1],r))+' + '+str(round(AxB[0],r))+'x' # tworzy podpis
		py.text(xP,yP,wektstr,family='serif',size=ts) # i plotuje go
	py.xticks(size=ts) # rozmiar cyfr
	py.yticks(size=ts)
	py.grid(True) # siatka
			
def niep_prad(wartosci,typ,p=1,r=3):
	'''Oblicza niepewnosci multimetrow dla kazdej z wartosci z listy,
	domyslne jest podanie wartosci w V/A/Ohm-ach.
	typ - str, jeden z IBRY,UBRY,OBRY,ICHY,UCHY,OCHY (case sensitive)
	wartosci - int,float,lista,krotka lub array
	p - przez jaka liczbe nalezy pomnozyc wartosc, aby otrzymac jednostke przykladowa?
		przyklad: mA = 0.001 A
	r - do ilu cyfr po przecinku zaokraglic?'''
	if not typ in ['IBRY','UBRY','OBRY','ICHY','UCHY','OCHY']: # jezeli zly typ, wywalamy
		raise Exception('Zle zdefiniowany multimetr i typ pomiaru')
	if type(wartosci) in [int,float]: wartosci = (wartosci,) # wartosci maja byc lista, tak bedzie latwiej
	typy = {'IBRY':((0.0004,2.0,0.0000005), # slownik: max wartosc dla przedzialu/procent/stala
					(0.0040,1.2,0.000003),
					(0.0400,2.0,0.00005),
					(0.4000,1.2,0.0003),
					(4.0000,2.0,0.005),
					(10.000,1.2,0.03)),
			'UBRY':((0.400,0.3,0.0004),
					(4.000,0.5,0.003),
					(40.00,0.5,0.03),
					(400.0,0.5,0,3),
					(1000.,1,4)),
			'OBRY':((4E2,0.8,0.6),
					(4E3,0.6,4E0),
					(4E4,0.6,4E1),
					(4E5,0.6,4E2),
					(4E6,1.0,4E3),
					(4E7,2.0,4E5)),
			'ICHY':((2E-4,1.,1E-7),
					(2E-3,1.,1E-6),
					(2E-2,1.,1E-5),
					(2E-1,1.,1E-4),
					(10.0,3.,1E-2)),
			'UCHY':((2E-1,.5,1E-4),
					( 2E1,.5,1E-3),
					( 2E2,.5,1E-2),
					( 2E3,.5,1E-1),
					( 6E3,.5,1.)),
			'OCHY':((2E3,0.8,0.3),
					(2E4,0.8,1.0),
					(2E5,0.8,1E2),
					(2E6,0.8,1E3),
					(2E7,3.0,4E4),
					(2E8,5.0,1E6))}
	zakresy = typy[typ] # wybieram konkretny zakres
	niepewnosci = np.zeros(len(wartosci)) # tworze wektor zer rowny dlugosci wartosciom
	for i in range(len(wartosci)): # dla kazdej z wartosci
		n = 0 
		while wartosci[i]*p > zakresy[n][0]: n += 1 # dopoki wartosc jest wieksza od zakresu ze slownika, ma sprawdzac kolejne zakresy
		niepewnosci[i] = (round((wartosci[i]*p*0.01*zakresy[n][1] + zakresy[n][2])/p,r)) #zaokragla wartosc razy procent i dodaje stala 
	return niepewnosci # zwraca wynik w takich samych jednostkach, jak poczatkowe

if __name__ == '__main__':
	A = np.arange(20,40)/10. # przykladowe dzialanie
	print list(niep_prad(A,'IBRY'))
