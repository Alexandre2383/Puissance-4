import numpy as np
import pygame
import sys
import math
import random

# Importation des bibliothèques nécessaires et initialisation des couleurs
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0) 
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Définition du nombre de lignes et de colonnes du jeu
ROW_COUNT = 6
COLUMN_COUNT = 7

# Définition des variables pour représenter les joueurs et les pièces
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4

# Fonction pour créer un plateau de jeu vide
def created_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Fonction pour placer une pièce dans une colonne donnée
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Fonction pour vérifier si une colonne est valide pour placer une pièce
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Fonction pour obtenir la première ligne ouverte dans une colonne donnée
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Fonction pour afficher le plateau de jeu avec une orientation inversée
def print_board(board):
    print(np.flip(board, 0))

# Fonction pour définir la difficulté du jeu
def get_difficulty():
    difficulty = None
    myfontDifficulty = pygame.font.SysFont("monospace", 28)
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                # Vérifier la zone de clic pour définir la difficulté
                if 50 < x < 150 and 200 < y < 300:
                    difficulty = 1  # Très facile
                elif 200 < x < 300 and 200 < y < 300:
                    difficulty = 2  # Facile
                elif 350 < x < 450 and 200 < y < 300:
                    difficulty = 3  # Normal
                elif 500 < x < 600 and 200 < y < 300:
                    difficulty = 4  # Difficile

        screen.fill(BLACK)
        # Dessiner les rectangles pour les niveaux de difficulté
        pygame.draw.rect(screen, GREEN, (50, 200, 100, 100))  # Très facile (vert)
        pygame.draw.rect(screen, YELLOW, (200, 200, 100, 100))  # Facile (jaune)
        pygame.draw.rect(screen, BLUE, (350, 200, 100, 100))  # Moyen (bleu)
        pygame.draw.rect(screen, RED, (500, 200, 100, 100))  # Difficile (rouge)
        # Dessiner les messages de difficulté
        label = myfontDifficulty.render("Very Easy", 1, WHITE)
        screen.blit(label, (20, 120))
        label = myfontDifficulty.render("Easy", 1, WHITE)
        screen.blit(label, (220, 120))
        label = myfontDifficulty.render("Normal", 1, WHITE)
        screen.blit(label, (350, 120))
        label = myfontDifficulty.render("Difficult", 1, WHITE)
        screen.blit(label, (470, 120))
        pygame.display.update()
    return difficulty

# Fonction pour vérifier si un joueur a gagné
def winning_move(board, piece):
    # Vérifier l'emplacement horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Vérifier l'emplacement vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Vérifier l'emplacement des diagonales positives
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Vérifier l'emplacement des diagonales négatives
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Fonction pour évaluer une fenêtre donnée et attribuer un score en fonction des pièces présentes
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

# Fonction pour attribuer un score global à la position actuelle du plateau
def score_position(board, piece):
    score = 0
    # Score colonne centrale
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score diagonale positive
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # Score diagonale négative
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    return score

# Fonction pour déterminer si le jeu est terminé
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_location(board)) == 0

# Algorithme minimax
def minimax(board, depth, maximizingPlayer):
    valid_location = get_valid_location(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_location)
        for col in valid_location:  
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_location)
        for col in valid_location:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

# Fonction pour obtenir toutes les colonnes valides
def get_valid_location(board):
    valid_location = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):  
            valid_location.append(col)
    return valid_location

# Fonction pour dessiner le plateau de jeu en utilisant Pygame
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

# Fonction pour réinitialiser le jeu avec un nouveau plateau
def reset_game():
    return np.array([[0] * COLUMN_COUNT for _ in range(ROW_COUNT)])

# Initialisation du plateau
board = created_board()
# Initialisation des conditions de la boucle de jeu
game_over = False
# Initialisation de Pygame
pygame.init()
# Initialisation des variables pour la taille de la fenêtre et le rayon des pièces
SQUARESIZE = 90
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)

myfontWin = pygame.font.SysFont("monospace", 75)
myfontReset = pygame.font.SysFont("monospace", 30)
# Initialisation de la fenêtre Pygame
size = (width, height)
screen = pygame.display.set_mode(size)
# Initialisation de la difficulté et de la profondeur du minimax
difficulty = get_difficulty()
depth = difficulty
# Sélection aléatoire du premier joueur
turn = random.randint(PLAYER, AI)

# Boucle principale du jeu
while not game_over:
    # Gestion des événements Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Suivi de la position de la souris pour le joueur actuel
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        # Détection du clic de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # Tour du joueur humain
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = myfontWin.render("Player 1 win!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    draw_board(board)
                    turn +=1
                    turn = turn % 2
        # Tour de l'IA
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, depth, True)
        if is_valid_location(board, col):
            pygame.time.wait(1000)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = myfontWin.render("Player 2 win!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            draw_board(board)
            turn +=1
            turn = turn % 2
    # Affichage du message de fin de jeu et gestion de la relance du jeu
    if game_over:
        draw_board(board)
        pygame.time.wait(3000)
        replay_text = myfontReset.render("Press Space to play or N to quit", 1, WHITE)
        screen.blit(replay_text, (10, 150))
        pygame.display.update()
        replay_decision = None
        while replay_decision is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        replay_decision = True
                    elif event.key == pygame.K_n:
                        replay_decision = False
        if replay_decision:
            # Initialisation d'un nouveau plateau
            board = reset_game()
            game_over = False
            difficulty = get_difficulty()
            depth = difficulty
            turn = random.randint(PLAYER, AI)
            draw_board(board)
        else:
            sys.exit()