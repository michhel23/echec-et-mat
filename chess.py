import numpy as np
import tkinter as tk


def convertir_position(position):
    colonne = ord(position[0].lower()) - 97  # Convertir la lettre en indice de colonne (a=0, b=1, ...)
    ligne = int(position[1]) - 1  # Convertir le chiffre en indice de ligne (1=0, 2=1, ...)
    return ligne, colonne

class Game:
    def __init__(self,fenetre):
        self.couleur_A,self.couleur_B = '#EBECD0',"#779556"
        self.tableau = np.zeros((8, 8))
        self.f = fenetre
        self.joueur_actuel = tk.IntVar(value=1) #1 blanc #2 noir
        self.emoji_pieces = {
            1: "♔",  # Roi blanc
            2: "♕",  # Reine blanche
            3: "♖",  # Tour blanche
            6: "♗",  # Fou blanc
            5: "♘",  # Cavalier blanc
            4: "♙",  # Pion blanc
            -1: "♚",   # Roi noir
            -2: "♛",   # Reine noire
            -3: "♜",   # Tour noire
            -6: "♝",   # Fou noir
            -5: "♞",   # Cavalier noir
            -4: "♟",    # Pion noir
            0: ""
        }
        self.click = []

    def initialiser_jeu(self):
        self.tableau[0, :] = [-3, -5, -6, -2, -1, -6, -5, -3]
        self.tableau[1, :] = -4
        self.tableau[2:6, :] = 0
        self.tableau[6, :] = 4
        self.tableau[7, :] = [3, 5, 6, 2, 1, 6, 5, 3]
        self.cases = []
        for i in range(9):
            ligne = []
            for j in range(9):
                if i == 8:
                    if j == 0:
                        case = tk.Label(self.f, text="", bg="white", width=4, height=2)
                    else:
                        case = tk.Label(self.f, text=chr(96 + j), bg="white", width=4, height=2)
                elif j == 0:
                    case = tk.Label(self.f, text=str(i+1), bg="white", width=4, height=2)
                else:
                    couleur = self.couleur_A if (i + j) % 2 == 0 else self.couleur_B  # Alterner les couleurs des cases
                    case = tk.Label(self.f, text="", bg=couleur, width=4, height=2)
                    case.config(highlightthickness=1,highlightbackground = couleur, highlightcolor= couleur)
                    case.bind("<Button-1>", lambda event, row=i, col=j: self.clic_case(event, row, col))
                case.grid(row=i, column=j)
                ligne.append(case)
            self.cases.append(ligne)
        
        self.maj_plateau()


        if self.joueur_actuel.get() ==  1:
            couleur = "blanc"
        else:
            couleur = "noir"
        
        self.couleur_tour = tk.Label(self.f, text=couleur)
        self.couleur_tour.grid(row=0, column=9, columnspan=2)

        self.instruction = tk.Label(self.f, text="cliquez sur la piece à déplacer")
        self.instruction.grid(row=1, column=9, columnspan=2)

        self.piece_choisie = tk.Label(self.f, text="piece choisie:")
        self.piece_choisie.grid(row=2, column=9, columnspan=2)

        self.arrivée = tk.Label(self.f, text="déplacement vers:")
        self.arrivée.grid(row=3, column=9, columnspan=2)

        self.warning = tk.Label(self.f, text="",bg='red')
        self.warning.grid(row=5, column=9, columnspan=2)

        # Créer un bouton pour jouer le coup et changer de joueur
        self.bouton_jouer = tk.Button(self.f, text="choisir", command=self.jouer_coup_et_changer_joueur, bg="white")
        self.bouton_jouer.grid(row=4, column=9, pady=5)

        self.Verif_eem = tk.Button(self.f, text="verif echec et mat", command=self.verif_echec_et_mat, bg="grey")
        self.Verif_eem.grid(row=7, column=9, pady=5)
        self.annonce_eem = tk.Label(self.f, text="")
        self.annonce_eem.grid(row=8, column=9, columnspan=2)

    def verif_echec_et_mat(self):
        if self.echec_et_mat() == True:
            self.annonce_eem.config(text="ECHEC ET MAT'!")
        else:
            self.annonce_eem.config(text="encore des coups sont jouables")

    def deplacer_piece(self, depart, arrivee):
        x_dep, y_dep = convertir_position(depart)
        x_arr, y_arr = convertir_position(arrivee)
        piece = self.tableau[x_dep, y_dep]
        if self.est_coup_valide(piece, x_dep, y_dep, x_arr, y_arr):
            self.tableau[x_arr, y_arr] = piece
            self.tableau[x_dep, y_dep] = 0
            return True
        else:
            return False

    def clic_case(self, event, row, col):
        nom_case = self.obtenir_nom_case(row, col-1).upper()
        case = self.cases[row][col]
        if len(self.click)==0:
            self.click.append(nom_case)
            pos = convertir_position(nom_case)
            emoji = self.emoji_pieces[self.tableau[pos[0],pos[1]]]
            self.piece_choisie.config(text=f"piece choisie:{emoji}-{nom_case}")
            self.bouton_jouer.config(text="incomplet",bg="orange")
            case.config(highlightthickness=1,highlightbackground = "green", highlightcolor= "green")
        elif len(self.click)==1:
            self.click.append(nom_case)
            self.arrivée.config(text=f"déplacement vers:{nom_case}")
            self.bouton_jouer.config(text="jouer",bg="green")
            case.config(highlightthickness=1,highlightbackground = "red", highlightcolor= "red")
        else:
            self.reset_button()
        

    def obtenir_nom_case(self, row, col):
        # Le plateau est numéroté de 0 à 7 horizontalement et verticalement
        lettres = "abcdefgh"
        numero_ligne = row+1
        lettre_colonne = lettres[col]
        return lettre_colonne + str(numero_ligne)

    def coordonnees_valides(self,x,y):
        if x>=0 and x<8 and y>=0 and y<8:
            return True 

    def piece_couleur(self,piece):
        if piece<0:
            return 2
        elif piece>0:
            return 1
        else:
            return 0

    def jouer_coup_et_changer_joueur(self):
        self.jouer_coup()

    def maj_plateau(self):
        for i in range(8):
            for j in range(8):
                piece = self.tableau[i, j]
                emoji_piece = self.emoji_pieces[piece]
                self.cases[i][j + 1].config(text=emoji_piece, font=("Arial", 25))

    def reset_button(self):
        self.click = []
        self.bouton_jouer.config(text="choisir",bg="white")
        self.piece_choisie.config(text="piece choisie:")
        self.arrivée.config(text="déplacement vers:")
        color, r =self.couleur_B,self.couleur_A
        for i in range(8):
            for j in range(8):
                self.cases[i][j + 1].config(highlightbackground = color, highlightcolor= color)
                color, r = r,color
            color, r = r,color

    def jouer_coup(self):
        if len(self.click)!=2:
            self.warning.config(text="choix invalide")
            self.reset_button()
        # Déplacer la pièce sur le plateau
        elif self.deplacer_piece(self.click[0], self.click[1]):
            # Mettre à jour les cases avec les pièces du plateau
            self.maj_plateau()
            
            self.reset_button()
            # Changer de joueur
            self.changer_joueur()
            self.warning.config(text="")
        else:
            self.warning.config(text="choix invalide")
            self.reset_button()
    
    def changer_joueur(self):
        if self.joueur_actuel.get() == 1:
            self.joueur_actuel.set(2)
            self.couleur_tour.config(text="noir")
        else:
            self.joueur_actuel.set(1)
            self.couleur_tour.config(text="blanc")
    
    
    def trouver_roi(self,roi,tableau):
        for x in range(8):
            for y in range(8):
                piece = tableau[x, y]
                if self.piece_en_lettre(piece) == roi:
                    return (x,y)
                
    
    def met_en_echec(self,x_dep, y_dep, x_arr, y_arr):
        # Fonction de vérification si le roi du joueur actuel est en échec
        # Retourne True si le roi est en échec, False sinon
        joueur = self.joueur_actuel.get()
        roi = "R" if joueur == 1 else "-R"
        tableau_cp = np.copy(self.tableau)
        tableau_cp[x_arr,y_arr] = tableau_cp[x_dep,y_dep]
        tableau_cp[x_dep,y_dep] = 0
        # Trouver les coordonnées du roi
        xy = self.trouver_roi(roi,tableau_cp)
        if xy == None:
            return True
        x_roi, y_roi = xy[0],xy[1]
        # Parcourir toutes les pièces de l'autre joueur pour vérifier si elles menacent le roi
        for x in range(8):
            for y in range(8):
                piece = tableau_cp[x, y]
                if piece != " " and self.piece_couleur(piece) != joueur:
                    if self.est_coup_valide(piece, x, y, x_roi, y_roi,joueur=1 if joueur==2 else 2,tableau = tableau_cp):
                        return True

        return False
    
    def echec_et_mat(self):
        for x in range(8):
            for y in range(8):
                piece = self.tableau[x, y]
                if piece != " " and self.piece_couleur(piece) == self.joueur_actuel.get():
                    for x1 in range(8):
                        for y1 in range(8):
                            if self.est_coup_valide(piece, x, y,x1,y1):
                                if not self.met_en_echec(x, y,x1,y1):
                                    return False
        return True
    

    def est_coup_valide(self, piece, x_dep, y_dep, x_arr, y_arr,joueur=None,tableau=None):
        if joueur==None and tableau==None:
            joueur = self.joueur_actuel.get()
            tableau = self.tableau
            if self.met_en_echec(x_dep, y_dep, x_arr, y_arr)==True:
                return False
        
        # Vérifier si les coordonnées de départ et d'arrivée sont valides
        if not self.coordonnees_valides(x_dep, y_dep) or not self.coordonnees_valides(x_arr, y_arr):
            return False
        
        # Vérifier si la case de départ contient une pièce appartenant au joueur actuel
        if tableau[x_dep, y_dep] != piece or self.piece_couleur(piece) != joueur:
            return False
        
        
        # Vérifier les règles de déplacement spécifiques à chaque type de pièce
        if self.piece_en_lettre(piece) == "P" or self.piece_en_lettre(piece) == "-P":
            # Règles de déplacement pour le pion
            """remplis les regles de déplacement du pion: 
            -ne peut pas reculer
            -s'il se trouve sur sa position de départ il a la possibilité d'avancer de 2 cases, sinon seulement d'une
            -s'il y'a une piece de l'autre joueur sur la case devant lui il ne peut pas pas avancer
            -il peut manger une piece seulement si celle-ci se trouve en diagonale en face de lui d'une case, il prends donc sa place
            -si le pion atteint la derniere case du plateau il se transforme en reine
            """
            joueur_pion = self.piece_couleur(piece)
            # Vérifier les déplacements en fonction du joueur du pion
            if joueur_pion == 1:  # Joueur blanc
                # Déplacement vers l'avant
                if y_arr == y_dep and x_arr == x_dep - 1 and tableau[x_arr, y_arr] == 0:
                    return True
                # Déplacement initial de 2 cases
                elif y_arr == y_dep and x_arr == x_dep - 2 and x_dep == 6 and tableau[x_dep - 1, y_arr] == 0 and tableau[x_arr, y_arr] == 0:
                    return True
                # Capture en diagonale
                elif abs(y_arr - y_dep) == 1 and x_arr == x_dep - 1 and self.piece_couleur(tableau[x_arr, y_arr]) == 2:  # Joueur noir
                    return True
            elif joueur_pion == 2:  # Joueur noir
                # Déplacement vers l'avant
                if y_arr == y_dep and x_arr == x_dep + 1 and tableau[x_arr, y_arr] == 0:
                    return True
                # Déplacement initial de 2 cases
                elif y_arr == y_dep and x_arr == x_dep + 2 and x_dep == 1 and tableau[x_dep + 1, y_arr] == 0 and tableau[x_arr, y_arr] == 0:
                    return True
                # Capture en diagonale
                elif abs(y_arr - y_dep) == 1 and x_arr == x_dep + 1 and self.piece_couleur(tableau[x_arr, y_arr]) == 1:  # Joueur blanc
                    return True

            return False

        elif self.piece_en_lettre(piece) == "-R" or self.piece_en_lettre(piece) == "R":
        # Règles de déplacement pour le roi
            if abs(x_arr - x_dep) <= 1 and abs(y_arr - y_dep) <= 1 and self.piece_couleur(tableau[x_arr, y_arr]) != joueur:
                return True

        elif self.piece_en_lettre(piece) == "C" or self.piece_en_lettre(piece) == "-C":
            # Règles de déplacement pour le cavalier
            dx = abs(x_arr - x_dep)
            dy = abs(y_arr - y_dep)
            if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
                return True

        elif self.piece_en_lettre(piece) == "F" or self.piece_en_lettre(piece) == "-F":
            # Règles de déplacement pour le fou
            dx = abs(x_arr - x_dep)
            dy = abs(y_arr - y_dep)
            if dx == dy:
                # Vérifier s'il n'y a pas de pièce entre le départ et l'arrivée
                if x_arr > x_dep and y_arr > y_dep:
                    for i in range(1, dx):
                        if tableau[x_dep + i, y_dep + i] != 0:
                            return False
                elif x_arr > x_dep and y_arr < y_dep:
                    for i in range(1, dx):
                        if tableau[x_dep + i, y_dep - i] != 0:
                            return False
                elif x_arr < x_dep and y_arr > y_dep:
                    for i in range(1, dx):
                        if tableau[x_dep - i, y_dep + i] != 0:
                            return False
                elif x_arr < x_dep and y_arr < y_dep:
                    for i in range(1, dx):
                        if tableau[x_dep - i, y_dep - i] != 0:
                            return False
                return True

        elif self.piece_en_lettre(piece) == "Q" or self.piece_en_lettre(piece) == "-Q":
            # Règles de déplacement pour la reine
            dx = abs(x_arr - x_dep)
            dy = abs(y_arr - y_dep)
            if dx == dy or x_dep == x_arr or y_dep == y_arr:
                # Vérifier s'il n'y a pas de pièce entre le départ et l'arrivée
                if dx == dy:
                    if x_arr > x_dep and y_arr > y_dep:
                        for i in range(1, dx):
                            if tableau[x_dep + i, y_dep + i] != 0:
                                return False
                    elif x_arr > x_dep and y_arr < y_dep:
                        for i in range(1, dx):
                            if tableau[x_dep + i, y_dep - i] != 0:
                                return False
                    elif x_arr < x_dep and y_arr > y_dep:
                        for i in range(1, dx):
                            if tableau[x_dep - i, y_dep + i] != 0:
                                return False
                    elif x_arr < x_dep and y_arr < y_dep:
                        for i in range(1, dx):
                            if tableau[x_dep - i, y_dep - i] != 0:
                                return False
                elif x_dep == x_arr:
                    if y_arr > y_dep:
                        for i in range(y_dep + 1, y_arr):
                            if tableau[x_dep, i] != 0:
                                return False
                    else:
                        for i in range(y_arr + 1, y_dep):
                            if tableau[x_dep, i] != 0:
                                return False
                elif y_dep == y_arr:
                    if x_arr > x_dep:
                        for i in range(x_dep + 1, x_arr):
                            if tableau[i, y_dep] != 0:
                                return False
                    else:
                        for i in range(x_arr + 1, x_dep):
                            if tableau[i, y_dep] != 0:
                                return False
                return True

        elif self.piece_en_lettre(piece) == "T" or self.piece_en_lettre(piece) == "-T":
            # Règles de déplacement pour la tour
            if x_dep == x_arr:
                # Vérifier s'il n'y a pas de pièce entre le départ et l'arrivée
                if y_arr > y_dep:
                    for i in range(y_dep + 1, y_arr):
                        if tableau[x_dep, i] != 0:
                            return False
                else:
                    for i in range(y_arr + 1, y_dep):
                        if tableau[x_dep, i] != 0:
                            return False
                return True
            elif y_dep == y_arr:
                # Vérifier s'il n'y a pas de pièce entre le départ et l'arrivée
                if x_arr > x_dep:
                    for i in range(x_dep + 1, x_arr):
                        if tableau[i, y_dep] != 0:
                            return False
                else:
                    for i in range(x_arr + 1, x_dep):
                        if tableau[i, y_dep] != 0:
                            return False
                return True
        # Si aucun cas spécifique n'est trouvé, le coup est invalide
        return False

    def piece_en_lettre(self, piece):
        if piece == 0:
            return ""
        elif piece == 1:
            return "R"
        elif piece == 2:
            return "Q"
        elif piece == 3:
            return "T"
        elif piece == 4:
            return "P"
        elif piece == 5:
            return "C"
        elif piece == 6:
            return "F"
        elif piece == -1:
            return "-R"
        elif piece == -2:
            return "-Q"
        elif piece == -3:
            return "-T"
        elif piece == -4:
            return "-P"
        elif piece == -5:
            return "-C"
        elif piece == -6:
            return "-F"





fenetre = tk.Tk()
fenetre.title("échecs scolaire")
plateau_jeu = Game(fenetre)
plateau_jeu.initialiser_jeu()


# Créer une étiquette pour le champ de saisie du coup


# Lancer la boucle principale de la fenêtre
fenetre.mainloop()