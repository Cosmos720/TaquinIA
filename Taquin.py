import copy
from random import shuffle
import time


POIDS = ((0, 36, 12, 12, 4, 1, 1, 4, 1),    #pi1
        (0, 8, 7, 6, 5, 4, 3, 2, 1),        #pi2 = pi3
        (0, 8, 7, 6, 5, 4, 3, 2, 1),        #pi3 = pi2
        (0, 8, 7, 6, 5, 3, 2, 4, 1),        #pi4 = pi5
        (0, 8, 7, 6, 5, 3, 2, 4, 1),        #pi5 = pi4
        (0, 1, 1, 1, 1, 1, 1, 1, 1))        #pi6

COEFF = (4, 1)  #rho1 à rho6

TESTS = [[1,7,3,4,2,6,5,0,8]]


class Taquin:

    """
    taille: La taille d'un coté du taquin
    heur: La liste des heuristiques utilisées
    cout: Le nombre de mouvement effectué pour atteindre l'état
    chemin: Les déplacements effectués pour atteindre l'état
    plateau: Les coordonnées des tuiles du taquin ainsi que les valeurs associées
    but: Les coordonnées des tuiles du taquin ainsi que les valeurs associées lorsqu'il est résolu
    moves: La listes des déplacements possibles
    f: La fonction d’évaluation : f(n) = g(n) + h(n) avec n le taquin actuel
    """

    def __init__(self, n, h):
        self.taille = n
        self.heur = h
        self.cout = 0
        self.chemin = "_"
        self.grille =[]
        self.plateau = {((j//n)+1, (j%n)+1):0 for j in range(n*n)}
        cpt = 1
        for i in self.plateau.keys():
            if i != (3, 3):
                self.plateau[i]=cpt
                cpt += 1
        for i in self.plateau.values():
            self.grille.append(i)
        self.but = copy.copy(self.plateau)
        self.moves = []
        self.f = self.calculer_f(self.heur)
    
    def afficher(self):
        format = ""
        for x in range(self.taille):
            liste = []
            for y in range(self.taille):
                liste.append(self.plateau[x+1, y+1])
            format += str(liste) + "\n"
        return format


    def est_solution(self):
        """Renvoie True si le taquin est résolu."""
        return self.plateau == self.but

    def chercher(self, e, but=False):
        """Retourne les coordonnées de la case e"""
        if(but):
            dico=self.but
        else:
            dico=self.plateau
        for i in dico.keys():
            if dico[i] == e:
                return i

    def bouger_trou(self, sens):
        """Déplace le trou dans l'une des directions Nord, Sud, Est, Ouest,
        et renvoie le taquin résultant avec le chemin et le cout mis à jour."""
        copie_T = copy.deepcopy(self)
        trou = self.chercher(0)
        if sens == "S":
            copie_T.plateau[trou] = self.plateau[(trou[0]-1, trou[1])]
            copie_T.plateau[(trou[0]-1, trou[1])] = self.plateau[trou]
            copie_T.chemin += "S"
        elif sens == "N":
            copie_T.plateau[trou] = self.plateau[(trou[0]+1, trou[1])]
            copie_T.plateau[(trou[0]+1, trou[1])] = self.plateau[trou]
            copie_T.chemin += "N"
        elif sens == "O":
            copie_T.plateau[trou] = self.plateau[(trou[0], trou[1]+1)]
            copie_T.plateau[(trou[0], trou[1]+1)] = self.plateau[trou]
            copie_T.chemin += "O"
        elif sens == "E":
            copie_T.plateau[trou] = self.plateau[(trou[0], trou[1]-1)]
            copie_T.plateau[(trou[0], trou[1]-1)] = self.plateau[trou]
            copie_T.chemin += "E"
    
        copie_T.cout += 1
        return copie_T

    def shuffleGrid(self):
        shuffle(self.grille)
        permutations = 0
        for i in range(len(self.grille)):
            for j in range(i+1, len(self.grille)):
                if self.grille[i]!=0 and self.grille[j]!=0:
                    if self.grille[i] > self.grille[j]:
                        permutations += 1
        if permutations%2 != 0:
            self.shuffleGrid()
        else:
            self.updateEtat()

    def setGrid(self, grille):
        self.grille=grille
        self.updateEtat()
    
    def updateEtat(self):
        i = 0
        for j in self.plateau.keys():
            self.plateau[j]=self.grille[i]
            i += 1

    def mvtPossible(self):
        self.moves=[]
        for k in self.plateau.keys():
            if self.plateau[k] == 0:
                if k[0]+1 <= self.taille:
                    self.moves.append("N")
                if k[0]-1 >= 1:
                    self.moves.append("S")
                if k[1]+1 <= self.taille:
                    self.moves.append("O")
                if k[1]-1 >= 1:
                    self.moves.append("E")

    def expanser(self):
        """Renvoie une liste des états accessibles à partir de l'état actuel."""
        childList = []
        self.mvtPossible()
        for move in self.moves:
            child = self.bouger_trou(move)
            childList.append(child)
        return childList
       
    def dist_elem(self, e):
        """Renvoie le nombre de cases séparant l'élément e de sa position 
        voulue. Fonction intermédiaire pour la distance de Manhattan."""

        d = 0
        position_actuelle = self.chercher(e)
        position_voulue = self.chercher(e, True)
        d = abs(position_actuelle[0] - position_voulue[0]) + abs(position_actuelle[1] - position_voulue[1])
        return d

    def manhattan(self, k):
        global POIDS, COEFF
        """Calcule la distance Manhattan avec POIDS[k] et COEFF[k].
        Fonction intermédiaire pour la fonction d'évaluation f."""
        somme = 0
        elem = [self.dist_elem(i) for i in range(len(self.plateau))]
        for h in k:
            somme += sum(POIDS[h-1][i] * elem[i] for i in range(len(self.plateau))) / COEFF[h%2]
        return somme

    def calculer_f(self, k):
        return self.cout + self.manhattan(k)
    
    def __repr__(self):
        toString = "\n"
        toString += self.afficher()
        toString += self.chemin + "\n"
        toString += str(self.f)
        return toString

    def aStar(self):
        taquin_creer = 1
        explored = Explored()
        pile = Frontiere()
        pile.ajouter(self)
        while(True):
            aExpanser = pile.etats.pop(0)
            if(aExpanser.est_solution()):
                print(("taquin crée = {}\n").format(taquin_creer))
                return aExpanser
            
            
            children = aExpanser.expanser()
            explored.ajouter(aExpanser)
            for child in children:
                taquin_creer += 1
                child.f = child.calculer_f(self.heur)
                if not(explored.contient(child)):
                    pile.ajouter(child)

class Frontiere:
    """Liste d'états triés selon leur valeur de f (ordre croissant)."""
    def __init__(self):
        self.etats = []

    def ajouter(self, e):
        """Ajoute e à la bonne position en fonction de sa valeur de f."""
        if self.etats == []:
            self.etats.insert(0,e)
        else:
            fait = False
            for i in range(len(self.etats)):
                if self.etats[i].f >= e.f and not fait:
                    self.etats.insert(i,e)
                    fait = True
            if not fait:
                self.etats.insert(len(self.etats),e)

class Explored:
    """Liste contenant les états déjà explorés"""
    def __init__(self):
        self.etats = []

    def ajouter(self, e):
        self.etats.append(e)

    def contient(self, e):
        for i in self.etats:
            if e.plateau == i.plateau:
                return True
        return False

class __main__:

    taille = 3
    heur = str(input("Heuristiques ?\nEntrez les numéros séparés par des espaces.\n"))
    if len(heur) == 1:
        heur = [int(heur)]
    else:
        heur = heur.split(' ')
        for index,choice in enumerate(heur):
            heur[index] = int(choice)
    t = Taquin(taille, heur)
    t.shuffleGrid()
    #t.setGrid([0,2,4,6,3,7,1,8,5])
    print(t)
    print(heur)
    start = time.time()
    result = t.aStar()
    print(("Duration : {}").format(time.time() - start))
    print(result)
    exit(0)

    