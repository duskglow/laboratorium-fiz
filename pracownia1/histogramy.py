#!/usr/bin/env python2
#-*- coding: utf-8 -*-

__author__ = 'Pawel Chojnacki'
__copyright__ ='Copyleft 2013 Pawel Chojnacki'
__version__ = '1.0'
__date__ = '15-03-2013'
__license__ = 'GPLv3'

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
		print sig, type(sig)
		sigma = sig*np.std(dane)
		print sigma,'lol',np.mean(dane)
		py.axvspan(np.mean(dane)-sigma,np.mean(dane)+sigma,alpha=.25)
	py.grid(True)
	if tyt!=0: py.title(tyt,family='serif')
	py.xticks(przedz,rotation=45)
	if osX!=0: py.xlabel(osX,family='serif')
	if osY!=0: py.ylabel(osY,family='serif')

def wiel_hist(dane,p=0,krok=0,norm=0,wys=0,osX=0,osY=0,sr=0,sig=0,tyt=0):
	'''Rysuje wiele histogramow w oknach identycznych z pierwszym
	dane - przyjmuje wektor wektorow danych o rownych dlugosciach'''
	# Przygotowanie identyncznych 
	if p==0: # Stworzenie przedzialow
		mini = min(min(dane[j]) for j in range(len(dane)))
		maks = max(max(dane[j]) for j in range(len(dane)))
		if krok == 0: krok = 1
		p = list(np.arange(mini,maks,krok))
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

pojedyncze = ['''TUTAJ WPISZ DANE''']

poczworne = ['''TUTAJ WPISZ DANE''']


podsumy = [ sum(pojedyncze[i:i+4])/4 for i in range(0,len(pojedyncze),4) ]

po4 = [ poczworne[i]/4 for i in range(len(poczworne))]

tytuly = [u'Histogram częstości okresów drgań wahadła - jeden pomiar',
u'Histogram częstości okresów drgań wahadła - średnia z czterech okresów pojedynczych',
u'Histogram częstości okresów drgań wahadła - średnia z pomiaru czterech okresów']

wiel_hist((pojedyncze,podsumy,po4),krok=0.03,norm=1,osX=u'Okres drgań [s]',osY=u'Częstość wystąpień [n]',sr=1,sig=1,tyt=tytuly)

py.figure(3)
histogram(pojedyncze,krok=0.01,norm=1,osX=u'Okres drgań [s]',osY=u'Częstość wystąpień [n]')

py.show()
