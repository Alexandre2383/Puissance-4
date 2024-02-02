import numpy as np
import pygame
import sys
import math
import random

#Import des bibliothèques nécessaires et définition de certaines constantes de couleur.

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0) 
#Définition du nombre de lignes et de colonnes du jeu Puissance 4.
ROW_COUNT = 6
COLUMN_COUNT = 7
#Définition de variables pour représenter le joueur humain (PLAYER), #l'intelligence artificielle (AI), les pièces du joueur et de l'IA, et des #constantes pour la taille de la fenêtre de vérification de victoire.
PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

WINDOW_LENGTH = 4
      
#Définition d'une fonction created_board pour initialiser un plateau de jeu vide.
def created_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

#Fonction drop_piece pour placer une pièce sur le plateau.
def drop_piece(board, row, col, piece):
    board[row][col] = piece
#Fonction is_valid_location pour vérifier si une colonne est valide pour placer #une pièce. 
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
#Fonction evaluate_window pour évaluer une fenêtre donnée et attribuer un score en fonction des pièces présentes.
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
        
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10
    
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 80
    
    return score
#Fonction score_position pour attribuer un score global à la position actuelle du plateau.
def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)


    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score
#Fonction get_valid_location pour obtenir toutes les colonnes valides où une pièce peut être placée.
def get_valid_location(board):
    valid_location = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_location.append(col)
    return valid_location
#Fonction pick_best_move pour choisir le meilleur coup possible pour l'IA en utilisant l'algorithme minimax simplifié.
def pick_best_move(board, piece):
    valid_location = get_valid_location(board)
    best_score = -1000
    best_col = random.choice(valid_location)
    for col in valid_location:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
            
    return best_col   
# Fonction draw_board pour dessiner le plateau de jeu et les pièces en utilisant la bibliothèque Pygame.
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE), width=0)
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):       
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Initialisation des paramètres pour la fenêtre Pygame, y compris la taille, le plateau de jeu initial, le joueur qui commence aléatoirement.
board = created_board()
game_over = False

pygame.init()

SQUARESIZE = 90
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE 

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)
#Boucle principale du jeu qui gère les événements de la souris, les mouvements des joueurs, et l'affichage des résultats.
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 win!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                        
                    draw_board(board)
                    
                    turn += 1
                    turn = turn % 2

    if turn == AI and not game_over:
        col = pick_best_move(board, AI_PIECE)

        if is_valid_location(board, col):
            pygame.time.wait(1000)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 win!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board)

            turn += 1
            turn = turn % 2
            
    if game_over:
        pygame.time.wait(3000)