#!/usr/bin/env python2
#-*- coding: utf-8 -*-
# GPLv3 by Pawel Chojnacki

import numpy as np
import pylab as py
	
def histogram(dane,przedz=0,krok=1,norm=0,wys=0,osX=0,osY=0,sr=0,sig=0,tyt=0):
	'''Rysuje histogram.
	przedz - przedzial do narysowania
	krok - krok histogramowania
	norm - normalizowac? T/F 
	sig  - rysowac zakresy ilu sigm?'''
	if not bool(przedz): przedz = np.arange(min(dane),max(dane),krok)
	if norm!=0: wagi = [1./len(dane)] * len(dane)
	else: wagi = [1.]*len(dane)
	if wys!=0: py.ylim((0,wys))
	py.hist(dane,bins=przedz,weights=wagi,color='gray')
	if sr!=0: py.axvline(np.mean(dane),color='black')
	if sig!=0: #przedzialy ufnosci
		sigma = sig*np.std(dane)
		msig,Msig = np.mean(dane)-sigma,np.mean(dane)+sigma
		py.axvspan(msig,Msig,alpha=.25)
		procent = sum(map(lambda d: msig < d <= Msig,dane)) / float(len(dane))
		print "W przedziale", sigma, "znajduje sie", procent
	py.grid(True)
	if tyt!=0:
		py.title(tyt,family='serif',size='x-large')
	py.xticks(przedz,rotation=45)
	if osX!=0: py.xlabel(osX,family='serif',size='large')
	if osY!=0: py.ylabel(osY,family='serif',size='large')

def wiel_hist(dane,p=0,krok=0,norm=0,wys=0,osX=0,osY=0,sr=0,sig=0,tyt=0):
	'''Rysuje wiele histogramow w oknach identycznych z pierwszym
	dane - przyjmuje wektor wektorow danych o rownych dlugosciach'''
	# Przygotowanie identyncznych 
	if p==0: # Stworzenie przedzialow
		mini = min(min(dane[j]) for j in range(len(dane)))
		maks = max(max(dane[j]) for j in range(len(dane)))
		if krok == 0: krok = 1
		p = list(np.arange(mini,maks,krok))
	# NORMALIZACJA
	wagi = []
	if norm==0:
		for i in range(len(dane)):
			wagi.append([1.] * len(dane[i]))
	else:
		for i in range(len(dane)):
			wagi.append(([1./len(dane[i])] * len(dane[i]))) 
	if wys==0: # Liczenie wysokosci wszystkich wykresow
		wys = max( max(np.histogram(dane[i],bins=p,weights=wagi[i])[0]) for i in range(len(dane)) )
		wys = wys * 1.1 # dziesiec procent wieksze
	#~ # ULADNIENIA
	if tyt!=0:
		if type(tyt)==tuple or type(tyt)==list: t = tyt
	for i in range(len(dane)):
		py.figure(i)
		if type(tyt)==list:
			histogram(dane[i],p,krok,norm,wys,osX,osY,sr,sig,tyt[i])
		else:
			histogram(dane[i],p,krok,norm,wys,osX,osY,sr,sig,tyt)
	
		
	

biny = 0.03 # bin, przedzial histogramu

pojedyncze = [
3.37, 3.34, 3.34, 3.37, 3.37, 3.34, 3.37, 3.31, 3.31, 3.38,
3.28, 3.37, 3.40, 3.37, 3.22, 3.35, 3.32, 3.40, 3.41, 3.35,
3.41, 3.21, 3.28, 3.38, 3.37, 3.37, 3.38, 3.43, 3.43, 3.40,
3.35, 3.28, 3.41, 3.37, 3.35, 3.44, 3.38, 3.43, 3.40, 3.47,
3.37, 3.38, 3.38, 3.40, 3.31, 3.40, 3.34, 3.35, 3.38, 3.44,
3.28, 3.34, 3.31, 3.44, 3.41, 3.44, 3.31, 3.44, 3.32, 3.40,
3.43, 3.44, 3.38, 3.34, 3.31, 3.50, 3.41, 3.44, 3.28, 3.34,
3.38, 3.38, 3.37, 3.40, 3.32, 3.35, 3.44, 3.34, 3.41, 3.38,
3.44, 3.28, 3.31, 3.44, 3.34, 3.34, 3.34, 3.41, 3.35, 3.37,
3.31, 3.31, 3.47, 3.31, 3.34, 3.44, 3.32, 3.47, 3.31, 3.34,
3.40, 3.29, 3.44, 3.38, 3.28, 3.41, 3.35, 3.37, 3.41, 3.41,
3.41, 3.34, 3.50, 3.41, 3.32, 3.44, 3.41, 3.31, 3.31, 3.37,
3.35, 3.47, 3.47, 3.41, 3.37, 3.44, 3.35, 3.41, 3.37, 3.38,
3.44, 3.34, 3.40, 3.40, 3.34, 3.38, 3.41, 3.40, 3.34, 3.34,
3.34, 3.40, 3.41, 3.44, 3.38, 3.50, 3.40, 3.35, 3.35, 3.37,
3.38, 3.34, 3.44, 3.41, 3.50, 3.37, 3.56, 3.41, 3.37, 3.32,
3.28, 3.43, 3.31, 3.29, 3.28, 3.43, 3.37, 3.41, 3.31, 3.37,
3.28, 3.44, 3.44, 3.40, 3.38, 3.41, 3.35, 3.40, 3.35, 3.41,
3.40, 3.37, 3.44, 3.41, 3.37, 3.44, 3.28, 3.34, 3.47, 3.31,
3.44, 3.34, 3.50, 3.38, 3.37, 3.41, 3.35, 3.34, 3.34, 3.38,
3.34, 3.35, 3.50, 3.44, 3.31, 3.34, 3.53, 3.41, 3.44, 3.47,
3.44, 3.37, 3.35, 3.44, 3.41, 3.35]

poczworne = [
13.22, 13.34, 13.44, 13.37, 13.34, 13.37, 13.25, 13.32, 13.34, 13.41,
13.43, 13.34, 13.31, 13.50, 13.46, 13.41, 13.32, 13.34, 13.41, 13.09,
13.34, 13.43, 13.41, 13.31, 13.31, 13.38, 13.38, 13.44, 13.28, 13.31,
13.31, 13.47, 13.35, 13.34, 13.32, 13.37, 13.56, 13.36, 13.37, 13.31,
13.44, 13.41, 13.50, 13.35, 13.44, 13.43, 13.60, 13.47, 13.35, 13.65,
13.50, 13.57, 13.47, 13.31]

dziesiatki = [ 33.35, 33.31, 33.32, 33.15, 33.34 ]
dz2 = [ 32.03, 31.91, 31.88, 31.94, 31.85 ] 
dz3 = [ 30.38, 30.35, 30.47, 30.40, 30.60 ]
dz4 = [ 29.13, 29.06, 29.04, 29.03, 28.97 ]
dz5 = [ 27.41, 27.41, 27.28, 27.69, 27.38 ]

podsumy = [ sum(pojedyncze[i:i+4])/4 for i in range(0,len(pojedyncze),4) ]

po4 = [ poczworne[i]/4 for i in range(len(poczworne))]

po10 = [ dziesiatki[i]/10 for i in range(len(dziesiatki))]

tytuly = [u'Histogram częstości okresów drgań wahadła\npomiar jednego okresu',
u'Histogram częstości okresów drgań wahadła\nśrednia z czterech okresów pojedynczych',
u'Histogram częstości okresów drgań wahadła\njedna czwarta pomiaru czterech okresów']

wiel_hist((pojedyncze,podsumy,po4),krok=0.03,norm='c',osX=u'Okres drgań [s]',osY=u'Częstość wystąpień [n]',sr=1,sig=1,tyt=tytuly)

#~ py.figure(4)
#~ histogram(pojedyncze,krok=0.01,norm=1,osX=u'Okres drgań [s]',osY=u'Częstość wystąpień [n]',
#~ tyt=u'Histogram częstości okresów drgań wahadła\nKrok co 0,01 s')

### DOKŁADNOŚĆ
#~ py.figure(4)
#~ dokl = [ pojedyncze[i]%10 for i in range(0,len(pojedyncze)) ]
#~ histogram(dokl,krok=1,osX=u'Ostatnia cyfra wartości pomiaru',osY=u'Częstość wystąpień [n]',
#~ tyt=u'Histogram częstości występowania poszczególnych cyfr\njako ostatnich znaczących przy pomiarze czasu')


print "Pojedyncze - srednia", round(np.mean(pojedyncze),2), "STD", round(np.std(pojedyncze),2), np.std(pojedyncze)/216
print "Srednai z czterech", round(np.mean(podsumy),2), "STD", round(np.std(podsumy),2), (np.std(podsumy))/54
print "Poczworne - srednia", round(np.mean(po4),2), "STD", round(np.std(po4),2), (np.std(po4))/54
print "Dziesiatki - srednia", round(np.mean(po10),2), "STD", round(np.std(po10),2), (np.std(po10))/5
print np.mean(dz2), np.std(dz2), np.std(dz2)/len(dz2)
print np.mean(dz3), np.std(dz3), np.std(dz3)/len(dz3)
print np.mean(dz4), np.std(dz4), np.std(dz4)/len(dz4)
print np.mean(dz5), np.std(dz5), np.std(dz5)/len(dz5)

raw_input()
py.show()
