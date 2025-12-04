#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_XXXX_YYYY_projet.py : CR projet « srabble », groupe ZZZ

XXXX <prenom.nom@etu-univ-grenoble-alpes.fr>
YYYY <prenom.nom@univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import random

# FONCTION DONNEES##############################################################
def symetrise_liste(lst) :
    """
    Auxilliaire pour Q1 : symétrise en place la liste lst.
    EB : modification de lst.

    >>> essai = [1,2] ; symetrise_liste(essai) ; essai
    [1, 2, 1]
    >>> essai = [1,2,3] ; symetrise_liste(essai) ; essai
    [1, 2, 3, 2, 1]
    """
    copie_lst = list(lst)
    for i in range(2, len(copie_lst)+1) : lst.append(copie_lst[-i])


def init_bonus() :
    """
    Q1) Initialise le plateau des bonus.
    """
    # Compte-tenu  de  la  double   symétrie  axiale  du  plateau,  on
    # a  7  demi-lignes  dans  le  quart  supérieur  gauche,  puis  la
    # (demi-)ligne centrale,  et finalement  le centre. Tout  le reste
    # s'en déduit par symétrie.
    plt_bonus = [  # quart-supérieur gauche + ligne et colonne centrales
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MT'],
        [''  , 'MD', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'MD', ''  , ''  , ''  , 'LD', ''],
        ['LD', ''  , ''  , 'MD', ''  , ''  , ''  , 'LD'],
        [''  , ''  , ''  , ''  , 'MD', ''  , ''  , ''],
        [''  , 'LT', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'LD', ''  , ''  , ''  , 'LD', ''],
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MD']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plt_bonus : symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plt_bonus)

    return plt_bonus


def generer_dictfr(nf=r'C:\Users\israe\OneDrive\Documents\Bruno.py\littre.txt'):
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    with Path(nf).open(encoding='utf_8') as fich_mots:
        for line in fich_mots:
            mots.append(line.strip().upper())
    return mots


def generer_dico() :
    """Dictionnaire des jetons.

    >>> jetons = generer_dico()
    >>> jetons['A'] == {'occ': 9, 'val': 1}
    True
    >>> jetons['B'] == jetons['C']
    True
    >>> jetons['?']['val'] == 0
    True
    >>> jetons['!']
    Traceback (most recent call last):
    KeyError: '!'
    """
    jetons = {}
    with Path(r'C:\Users\israe\OneDrive\Documents\Bruno.py\lettres.txt').open(encoding='utf_8') as lettres:
        for ligne in lettres:
            l, v, o = ligne.strip().split(';')
            jetons[l] = {'occ': int(o), 'val': int(v)}
    return jetons


# CONSTANTES ###################################################################
TAILLE_PLATEAU = 15  # taille du plateau de jeu
TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)
JOKER = '?'  # jeton joker

dico=generer_dico()

# PARTIE 1

def init_jetons(): # Question 2
    j = [["" for i in range(TAILLE_PLATEAU)] for i in range(TAILLE_PLATEAU)]
    return j


def affiche_jetons(j, bonus_plateau=None): # Question 3 et 4
    if bonus_plateau is None:
        bonus = init_bonus()
    else:
        bonus = bonus_plateau
        
    taille = len(j)
    LD = '°'
    LT = '^'
    MD = '²'
    MT = '*' 
    # correction : ne pas réinitialiser bonus ici (on utilise le bonus passé)
    # bonus = init_bonus()

    print("    ", end="")
    for col in range(1, taille + 1):
        
        # nomenclature de colonne

        if col < 10:
            print("0" + str(col) + " ", end="")
        else:
            print(str(col) + " ", end="")
    print()
    print("   " + "|---" * taille + "|")

    

    for ligne in range(taille):
        
        # nomenclature de ligne

        if ligne + 1 < 10:
            print("0" + str(ligne + 1) + " ", end="")
        else:
            print(str(ligne + 1) + " ", end="")

        for col in range(taille):
            case = j[ligne][col]
            case_b = bonus[ligne][col]

            if case == "":
                case = " "
                if case_b == "LD":
                    case = LD
                elif case_b == "LT":
                    case = LT
                elif case_b == "MD":
                    case = MD
                elif case_b == "MT":
                    case = MT
            else:
                if case_b != "":
                    case += "*"
           
            if len(case) == 1:   #pour eviter que le tableau se deforme a cause de la diff de taille
                case += " "

            # affichage de la case
            print("| " + case, end="")

        print("|")  
        print("   " + "|---" * taille + "|")

j = init_jetons()
affiche_jetons(j,bonus_plateau=None) 


def plateau():  # Question 5
    j = init_jetons()
    return j 

# PARTIE 2

def init_pioche_alea(): # Question 7 

    l1=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    # on s'assure qu'il y est toute les lettres au moins une fois

    P=[JOKER,JOKER,]+l1
    
    # on remplie aléatoirement jusqu'à 100 jetons
    
    for i in range(0,72):
        x=random.randint(0,25)
        P.append(l1[x])
    return P
sac2=init_pioche_alea() # Question 8

def piocher(x, sac):
    L = []
    for ind in range(0, x):
        if len(sac) == 0:
            return L
        p = random.randrange(len(sac))
        L.append(sac.pop(p))
    return L


def completer_main(main, sac): # Question 9
    cm=7-len(main)
    if cm <= 0:
        return main
    if len(sac) <= cm:
        # On prend tout ce qu'il reste 
        for i in sac:
            main.append(i)
    else:
        d=piocher(cm, sac)
        main=main+d
    return main


def echanger (jetons, main, sac): # Question 10
    R=True
    # on enleve les jetons de la main 
    jetons_retires = []
    for x in jetons:
        if x in main:
            main.remove(x)
            jetons_retires.append(x)

    # on remet les jetons retirés dans le sac et on mélange
    sac.extend(jetons_retires)
    random.shuffle(sac)

    main2=completer_main (main, sac)
    if len(main2)<7:
        R=False
    if R:
        print("l'échange est réussi",R,)
    else:
        print("l'échange a échoué",R,)
    return main2


def sim_partie(): # Question 11
    J1=piocher(7, sac2)      
    print("J1 = ",J1)
    print()
    J2=piocher(7, sac2)


    e=input("J1 voulez vous échangez vos jetons  O/N  ")
    jetons1=[]
    jetons2=[]


    if e== 'O':
        c=1
        j=input("Entrer les jetons a échanger  ")
        while j!='!'and c<=7:
            jetons1.append(j)
            c=c+1
            j=input("Entrer les jetons a échanger  ")
        J1=echanger(jetons1, J1, sac2)
        c=1 
    print("J1 = ",J1)   
    print("Il reste ",len(sac2),"jetons dans le sac")
    print()

    print("J2 = ",J2)
    print()
    e=input("J2 voulez vous échangez vos jetons  O/N  ")
    if e== 'O':
        c=1
        j=input("Entrer les jetons a échanger  ")
        while j!='!'and c<=7:
            jetons2.append(j)
            c=c+1
            j=input("Entrer les jetons a échanger  ")
        J2=echanger (jetons2, J2, sac2)
    print("J2 = ",J2)
    print()
    print("Il reste ",len(sac2),"jetons dans le sac")


# PARTIE 3

def select_mot_initiale(motsfr,let): # Question 13
    l=[]
    for i in motsfr:
        if i[0]==let:
          l.append(i)
    return l


def select_mot_longueur(motsfr,lgr): # Question 14
    l=[]
    for i in motsfr:
        if len(i)==lgr:
            l.append(i)
    return l


def mot_jouable(mot,ll,lp):
    P=True
    jok=ll.count(JOKER)   # on regarde le nombre de joker
    lettre = ll.copy()  # pour pas modifier ll
    mot = list(mot)
    lp = list(lp)

    for x in lp:
        if x in mot:
            mot.remove(x)
        
    for i in mot:
        if i in lettre:
            lettre.remove(i)  # pour eviter de reutiliser des lettre)
        elif JOKER in lettre:
            lettre.remove(JOKER) # on utilise un joker 
        else:
            P=False
    return P


def mot_jouables(motsfr,ll,lp): 
    l=[]
    for i in motsfr:
        m=mot_jouable(i,ll,lp)
        if m :
            l.append(i)
    return l


def init_pioche(dico):
    l=[]
    for i in dico:
        x=dico[i]['occ']
        l.append(x*i)

    lj=[]
    for i in l:
        for x in i:
            lj.append(x)
    return lj


def mot_jouable2(mot,main): # Question 15 et 17 et 18
    P=True
    jok = main.count(JOKER)   # on regarde le nombre de joker
    lettre = main.copy()  # pour pas modifier ll
    mot = list(mot)
        
    for i in mot:
        if i in lettre:
            lettre.remove(i)  # pour eviter de reutiliser des lettre)
        elif JOKER in lettre:
            lettre.remove(JOKER) # on utilise un joker 
        else:
            P=False
    return P


def mot_jouables2(motsfr,main): # Question 16
    l=[]
    for i in motsfr:
        m=mot_jouable2(i,main)
        if m :
            l.append(i)
    return l

motsfr = generer_dictfr()
sac=init_pioche(dico)

# PARTIE 4

def valeur_mot(mot,dico): # Question 22
    pt=0
    if len(mot)==7:
        pt=50
    else:
        pt=0
    for k in mot:
        val=dico[k]['val']
        pt=pt+val
    return pt


def meilleur_mot(motsfr, ll, dico, lp): # Quetions 23 Et 24 !!!!!!!!!bug avec les joker a corrriger!!!!!!!
    lmj = mot_jouables(motsfr, ll, lp)
    if not lmj:
        return []
    
    scores = [valeur_mot(m, dico) for m in lmj]
    pmax = max(scores)
    return [m for m in lmj if valeur_mot(m, dico) == pmax]

# PARTIE 5

def tour_joueur(main,lp=''): # Question 25
    print(plateau())
    jetons_e=[]
    coup=input("que voulez vous faire (passer/echanger/proposer )")
    if coup=="echanger":
        j=input("Entrer les jetons a échanger  ")
        while j!='!':
            j=input("Entrer les jetons a échanger  ")
            jetons_e.append(j)
        main=echanger (jetons_e, main, sac)
        return main
    elif coup=='proposer':
        valeur=0
        mot=input('Quelle mot proposer vous ? :  ')
        if mot in mot_jouables(motsfr,main,lp):
            valeur=valeur_mot(mot,dico)
        return [valeur,mot] 
    else:
        print("fin du tour")
    print('Joueur suivant')


def detecte_fin_partie2(sac): # Question 26
    if len(sac)==0:
        print('Fin de partie')

def malus(liste_j,dico):
    pt=0
    for lettre in liste_j:
        val=dico[lettre]['val']
        pt=pt+val
    return pt

def detecte_fin_partie(sac, joueurs, dico): # Question 26
    
    # On s'assure que la partie soit terminer
    if len(sac)==0:
        print('Fin de partie')

        # on calcul les malus
        liste_malus=[]
        pt=0
        for nom in joueurs:
            pt=0
            for lettre in joueurs[nom]:
                val=dico[lettre]['val']
                pt=pt+val
                liste_malus=[].append(pt)
        
        # On calcul les vrai scores
        for nom in joueurs:
            for i in liste_malus:
                joueurs[nom]['score']= joueurs[nom]['score']-i
        
        # Présenttion des résultat et du gagnant
        liste_score=[]
        print(nom,'a',joueurs[nom]['score'],'points')
        for nom in joueurs:
            print(nom,'a',joueurs[nom]['score'],'points')
            liste_score.append(joueurs[nom]['score'],dico)
        for nom in joueurs:
            if joueurs[nom]['score']==max(liste_score):
                Gagnant=nom       
        print('Le gagnant est',Gagnant,'avec',joueurs[Gagnant]['score'],'points !!!')

def partie(): # Quetion 28
    
    # on crée les joueurs
    nb_joueur=int(input('Nombre de joueur : '))
    joueurs={}
    for i in range(nb_joueur): 
        J=input('Saisissez les nom des joueurs :  ')
        joueurs[J] = {"main": [], "score": 0}

     # on crée la pioche
    sac=init_pioche(dico) 
    
    # début de partie
    for nom in joueurs:
        joueurs[nom]["main"].extend(piocher(7, sac))
        print('Voila votre main ',joueurs[nom]["main"])
    print()
    # on crée le plateau
    plat=plateau() 
    while len(sac)>0:
        for nom in joueurs:
            print('Au tour de ',nom, 'de jouer')
            T=tour_joueur(joueurs[nom]["main"],lp='')
            
            # On vérifie que le joueur a choisie de proposer un mot
            if len(T)==2 : 
                joueurs[nom]["score"]+=T[0]
                n_main=joueurs[nom]["main"].copy() # Pour s'assurer de pas retirer plusieurs fois la lettre
                for lettre in T[1]:
                    if lettre in n_main: 
                        n_main.remove(lettre)
                n_main=completer_main (n_main, sac)
                joueurs[nom]["main"]=n_main
                print(joueurs[nom],joueurs[nom]["main"],joueurs[nom]["score"])
            
            # Cas ou le joueur a choisie échanger
            elif T!=None and T!=2:
                print('Voila ta nouvelle pioche',T,)
    detecte_fin_partie2(sac)

    # Fin de partie le sac est vide
    liste_score=[]
    print(nom,'a',joueurs[nom]['score'],'points')
    for nom in joueurs:
        liste_score.append(joueurs[nom]['score']-malus(joueurs[nom]['main'],dico))
    for nom in joueurs:
        if joueurs[nom]['score']-malus(joueurs[nom]['main'],dico)==max(liste_score):
            Gagnant=nom       
    print('Le gagnant est',Gagnant,'avec',joueurs[Gagnant]['score'],'points !!!')

# PARTIE 6

def lire_coords(plat): # Question 29
    i = int(input('Entrer une coordonnée ligne (1..15) : ')) - 1
    j = int(input('Entrer une coordonnée colonne (1..15) : ')) - 1
    while not (0 <= i < TAILLE_PLATEAU and 0 <= j < TAILLE_PLATEAU) or (plat[i][j] != '' and plat[i][j] not in '²*°^'):
        i = int(input('Entrer une coordonnée ligne valide (1..15) : ')) - 1
        j = int(input('Entrer une coordonnée colonne valide (1..15) : ')) - 1
    return i, j


def tester_placement(plat, i, j, direction, mot):  # Question 30
    lettres = []

    if direction == 'horizontal':
        for k, c in enumerate(mot):
            # vérification bornes
            if not (0 <= j+k < TAILLE_PLATEAU):
                return []
            case = plat[i][j+k]
            if case == '':
                lettres.append(c)
            elif case == c:
                lettres.append(c + '!')   # On marque que la lettre est déjà présente
            else:
                return []                 # Placement impossible

    elif direction == 'vertical':
        for k, c in enumerate(mot):
            # vérification bornes
            if not (0 <= i+k < TAILLE_PLATEAU):
                return []
            case = plat[i+k][j]
            if case == '':
                lettres.append(c)
            elif case == c:
                lettres.append(c + '!')   
            else:
                return []                 

    return lettres



def placer_mot(plat, main, i, j, direction, mot, bonus_plateau):  # Question 31
    lettres = tester_placement(plat, i, j, direction, mot)

    if lettres != []:
        if direction == 'horizontal':
            for k, l in enumerate(lettres):
                if '!' in l:    # On regarde si la lettre est deja presente grace a la marque
                    plat[i][j+k] = l[0]   # on place la lettre sans le !
                elif l in main:
                    plat[i][j+k] = l
                    main.remove(l)
                elif JOKER in main:
                    # le joker prend la valeur de la lettre (on place la lettre en minuscule pour marquer le joker)
                    plat[i][j+k] = "?"
                    main.remove(JOKER)

        elif direction == 'vertical':
            for k, l in enumerate(lettres):
                if '!' in l:    
                    plat[i+k][j] = l[0]
                elif l in main:
                    plat[i+k][j] = l
                    main.remove(l)
                elif JOKER in main:
                    plat[i+k][j] = l.lower() # On place le joker en minuscule au cas ou quelqu'un forme un mot a partir de ce joker
                    main.remove(JOKER)

        return True
    else:
        return False



def valeur_mot2(plat, main, i, j, direction, mot, dico, bonus_plateau):  # Question 32
    
    BMD = False
    BMT = False

    pt = 0

    # On regarde si le joueur utilise tous ses jetons 
    if len(main) == 0:
        pt = pt + 50

    if direction == 'horizontal':

        for k, l in enumerate(mot):
            
            # si la lettre a été placée via un joker, elle est en minuscule sur le plateau
            lettre_plateau = plat[i][j+k]
            # utiliser la lettre réelle en majuscule pour consulter le dictionnaire
            if isinstance(lettre_plateau, str) and lettre_plateau != '':
                lettre_val = '?'
            else:
                lettre_val = l
            val = dico[lettre_val]['val']
            bonus_case = bonus_plateau[i][j+k] # On teste la case pour voir si c'est un bonus ou non

            # Bonus lettre
            if bonus_case == 'LD':
                val = val*2
                bonus_plateau[i][j+k] = ''
            elif bonus_case == 'LT':
                val = val*3
                bonus_plateau[i][j+k] = ''

            # Bonus mot
            elif bonus_case == 'MD':
                BMD = True
                bonus_plateau[i][j+k] = ''
            elif bonus_case == 'MT':
                BMT = True
                bonus_plateau[i][j+k] = ''
            pt = pt + val

        if BMD:
            pt = pt*2
        if BMT:
            pt = pt*3

    elif direction == 'vertical':

        for k, l in enumerate(mot):
            lettre_plateau = plat[i+k][j]
            if isinstance(lettre_plateau, str) and lettre_plateau != '':
                lettre_val = lettre_plateau.upper()
            else:
                lettre_val = l
            val = dico[lettre_val]['val']
            bonus_case = bonus_plateau[i+k][j]

            if bonus_case == 'LD':
                val = val*2
                bonus_plateau[i+k][j] = ''
            elif bonus_case == 'LT':
                val = val*3
                bonus_plateau[i+k][j] = ''
            elif bonus_case == 'MD':
                BMD = True
                bonus_plateau[i+k][j] = ''
            elif bonus_case == 'MT':
                BMT = True
                bonus_plateau[i+k][j] = ''
            pt = pt + val

        if BMD:
            pt = pt*2
        if BMT:
            pt = pt*3

    return pt



# PARTIE 7

def tour_joueur2(plat, main,): #Question 34 
    affiche_jetons(plat, bonus_plateau)
    jetons_e=[]
    coup=input("que voulez vous faire (passer/echanger/proposer )")
    if coup=="echanger":
        j=input("Entrer les jetons a échanger  ")
        while j!='!':
            j=input("Entrer les jetons a échanger  ")
            jetons_e.append(j)
        main=echanger (jetons_e, main, sac)
        return main
    
    elif coup=='proposer':
        valeur=0
        i=int(input('entrer les coordonnées de la ligne : ')) 
        j=int(input('entrer les coordonnées de la colonne : ')) 
        direction=input('Entrer une direction (vertical/horizontal) : ')
        print(mot_jouables2(motsfr,main))
        mot=input('Quelle mot proposer vous ? :  ')

        # on vérifie d'abord que le mot est jouable avec la main puis on tente le placement
        while not (mot in mot_jouables2(motsfr,main) and placer_mot(plat,main, i, j, direction, mot, bonus_plateau)):
           mot=input('Quelle mot proposer vous ? :  ')
        valeur=valeur_mot2(plat,main, i, j, direction, mot, dico, bonus_plateau) 
        return [valeur,mot] 
    
    else:
        print("fin du tour")
    print('Joueur suivant')


# Question 35 PROGRAMME PRINCIPAL

# on crée les joueurs
nb_joueur=int(input('Nombre de joueur : '))
joueurs={}
for i in range(nb_joueur): 
    J=input('Saisissez les nom des joueurs :  ')
    joueurs[J] = {"main": [], "score": 0}

# On crée la pioche
sac=init_pioche(dico) 
    
# début de partie
for nom in joueurs:
    joueurs[nom]["main"].extend(piocher(7, sac))
    print('Voila votre main ',nom ,joueurs[nom]["main"])
print()

# on crée le plateau
bonus_plateau = init_bonus()
plat=plateau() 
while len(sac)>0:
    for nom in joueurs:
        print('Au tour de ',nom, 'de jouer')
        T=tour_joueur2(plat,joueurs[nom]["main"])
            
        # On vérifie que le joueur a choisie de proposer un mot
        if len(T)==2 : 
            joueurs[nom]["score"]+=T[0]
            joueurs[nom]["main"]=completer_main (joueurs[nom]["main"], sac)
            print(joueurs[nom],joueurs[nom]["main"],joueurs[nom]["score"])
            affiche_jetons(plat, bonus_plateau)
            
        # Cas ou le joueur a choisie échanger
        elif T!=None and T!=2:
            print('Voila ta nouvelle pioche',T,)

# Fin de partie le sac est vide
detecte_fin_partie(sac, joueurs, dico)


