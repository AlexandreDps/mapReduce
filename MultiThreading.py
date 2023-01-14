# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/python

import threading
import time
import math
import requests
from bs4 import BeautifulSoup

url = 'https://fr.wikipedia.org/wiki/Python_(langage)'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
sometext = soup.get_text()

start = time.time()
mots = sometext.split() 
mots2 = list(set(sometext.split())) #On s'en sert pour les reducer
nbpaquets = 5
taille_division = math.ceil(len(mots)/nbpaquets)
aftermap = [] #liste dans laquelle on va stocker les mots après mapping
afterreduce = {} #resultat
listeFred = [] #Liste de nos threads
mapped = threading.Event()

class Thread(threading.Thread):
    def __init__(self,ID,name,fonction):
        global mots
        global mots2
        global listeFred
        threading.Thread.__init__(self)
        listeFred.append(self)
        self.ID = ID
        self.name = name
        self.fonction = fonction
    
    def run(self):
        if self.fonction == 'mapper' :
            if len(mots) > 0 : 
                mapper(self.name)
                print(self.name + ' done\n')
            #Si il reste des mots a mapper, les thread ayant finit de mapper 
            #en premier continuent de mapper ce qu'il reste
            if len(mots) > 0 : 
                self.run()
            else : #sinon ils deviennent reducer pour la suite
                self.set_fonction('reducer')
                print(self.name + " attends que tous les fred aient fini de mapper\n")
                if checkMapping(listeFred):
                    print('Les freds ont fini de mapper !')
                    mapped.set() #On déclenche l'évenement mapped, permettant aux thread de continuer
                else:
                    mapped.wait()
            
                self.run()
            
        elif self.fonction == 'reducer' :
            try : 
                reducer(self.name)
                print(self.name + ' done\n')
            except : pass
            if len(mots2) > 0 :
                try: 
                    self.run()
                except:pass
            else :
                print(self.name + ' est mort\n')
            
    def set_fonction(self,fonction):
        self.fonction = fonction
    
def mapper(nom):
    global mots
    global aftermap
    time.sleep(0.1)
    print(nom + ' is Mapping\n')
    if len(mots)>taille_division :
        paquet = mots[:taille_division]
        mots = mots [taille_division:]
        for i in list(set(paquet)) :
            aftermap.append({i: paquet.count(i)})
    else :
        paquet = mots
        mots = []
        for i in list(set(paquet)) :
            aftermap.append({i: paquet.count(i)})

def reducer(nom):
    global aftermap
    global mots2
    global afterreduce
    print(nom + ' is reducing\n')
    time.sleep(0.1)
    mot = mots2.pop(0)
    compteur = 0
    for i in aftermap :
        if list(i.keys())[0] == mot:
            compteur += list(i.values())[0]
            aftermap.remove(i)
    afterreduce[mot] = compteur

def checkMapping(listeFred):
    continuer = True
    for i in listeFred:
        if i.fonction == 'mapper': #Si il reste un mapper on l'attends
            continuer = False
    return continuer


nombredefred = 10
for i in range(nombredefred):
    newFred = Thread(i, "Fred" + str(i), 'mapper')  

for i in listeFred :
    i.start()

for i in listeFred :
    i.join()

end = time.time()
sorted_dict = dict(sorted(afterreduce.items(), key=lambda item: item[1], reverse=True))
print('Après un commun effort, les freds ont construit ce dictionnaire pour vous :')
print(sorted_dict)
print("Les Freds ont travaillé " + str(end-start) + " secondes")

        
        