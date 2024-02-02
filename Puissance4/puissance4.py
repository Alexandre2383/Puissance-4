import numpy as np
import pygame
import sys
import math

#Import des bibliothèques nécessaires et définition de certaines constantes de couleur.
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0) 
#Définition du nombre de lignes et de colonnes du jeu Puissance 4.
ROW_COUNT = 6
COLUMN_COUNT = 7
#Définition d'une fonction created_board qui initialise un plateau de jeu vide avec des zéros.
def created_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
#Fonction drop_piece pour déposer une pièce (jeton) sur le plateau.
def drop_piece(board, row, col, piece):
    board[row][col] = piece
#Fonction is_valid_location pour vérifier si une colonne est valide pour placer une pièce.
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
#Fonction get_next_open_row pour obtenir la première ligne ouverte dans une colonne donnée.
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
#Fonction print_board pour afficher le plateau de jeu avec une orientation inversée (rotation de 180 degrés).
def print_board(board):
    print(np.flip(board, 0))
#Fonction winning_move pour vérifier si le joueur ayant la pièce spécifiée a gagné.
def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
             if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                 return True
             
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
             if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                 return True
                     
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
             if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                 return True

    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
             if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                 return True
             
# Fonction draw_board pour dessiner le plateau de jeu avec les pièces dans la fenêtre Pygame.
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE), width=0)
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):       
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

#Initialisation du plateau, du statut du jeu (game_over), et du tour actuel.
board = created_board()
game_over = False
turn = 0
#Initialisation de Pygame.
pygame.init()
#Définition des dimensions de la fenêtre Pygame.
SQUARESIZE = 90
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
#Définition de la taille de la fenêtre Pygame, du rayon des pièces, création de la fenêtre, dessin du plateau et mise à jour de l'affichage.
size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)

draw_board(board)

pygame.display.update()
#Définition d'une police pour le texte dans la fenêtre Pygame.
myfont = pygame.font.SysFont("monospace", 75)
#Boucle principale du jeu, qui gère les événements Pygame, tels que la fermeture de la fenêtre.
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
#Gestion du mouvement de la souris pour afficher la position potentielle de la pièce à placer.
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
#Gestion du clic de souris pour placer une pièce lorsque c'est le tour du joueur.
#python
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # print(event.pos)
            #Ask for palyer 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
#Vérification si le mouvement est valide, mise à jour du plateau, vérification de la victoire du joueur 1.
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 win!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
# Tour du joueur 2, vérification de la validité du mouvement, mise à jour du plateau, vérification de la victoire du joueur 2.
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board, 2):
                        label = myfont.render("Player 2 win!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
#Mise à jour du plateau après chaque coup et changement de tour.
            draw_board(board)
            turn +=1
            turn = turn % 2
#Attente de 3 secondes après la fin du jeu avant de quitter
            if game_over:
                pygame.time.wait(3000)