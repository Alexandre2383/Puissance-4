import numpy as np
import pygame
import sys
import math
import random
# Color initialization
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0) 

# number of row and colomn of the game
ROW_COUNT = 6
COLUMN_COUNT = 7

#Variable to define which turn to play 
PLAYER = 0
AI = 1

# Input in the board
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0

# number to win
WINDOW_LENGTH = 4

#create our board function
def created_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))#our dimensional board, with 0 we have 7 for y, 7+0=8 for x
    return board

# drop piece in the right row/column
def drop_piece(board, row, col, piece):
    board[row][col] = piece

#function check if Player input is valid     
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

#check board position equal 0
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

#change the orientation of the board = 180°
def print_board(board):
    print(np.flip(board, 0))
    
#Winning condition
def winning_move(board, piece):
    # check horizontal location
    for c in range(COLUMN_COUNT-3):#COLUMN_COUNT-3 because you can't win with 3 power
        for r in range(ROW_COUNT):
             if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                 return True
             
    # check vertical condition
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):#ROW_COUNT-3 because you can't win with 3 power
             if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                 return True
             
    #Check positive diaganols location         
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):#ROW_COUNT-3 because you can't win with 3 power
             if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                 return True

    #check negative diaganols location
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):#3 because negative diaganols can't begin 1 and 3
             if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                 return True
             
def evaluate_window(window, piece):
    score = 0
    # opp_piece represent the opponent piece
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
        
    # if window.count(piece) == 4:
    #     score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    
    return score
             
def score_position(board, piece):
    score = 0
    # Score  center column   
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

                
    # Score positive diaganol
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    
    # Score negative diaganol
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    
    return score

# Check if Player or AI win, or if len(get_valid_location(board)) == 0 the game end within a victory
def is_terminal_node(board):# if True, it is a terminal node
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_location(board)) == 0

# Algorithm minimax, possible moove tree * depth
def minimax(board, depth, maximizingPlayer):
    valid_location = get_valid_location(board) # 
    is_terminal = is_terminal_node(board) # if False, then continue
    if depth == 0 or is_terminal:# Stop the recursive function
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else:# Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:
        value = -math.inf # giving an infinite value is a security for next step
        column = random.choice(valid_location) # choose a valid random location for column
        for col in valid_location:  
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1] # return the best score of recursive function minimax
            if new_score > value:
                value = new_score
                column = col
        return column, value # return the best value with the column choice
        
    else: # Minimizing player
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
# Check all valid column 
def get_valid_location(board):
    valid_location = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):  
            valid_location.append(col)
    return valid_location

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
             
# For print board in pygame
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

board = created_board()
#initialize Game loop condition
game_over = False

#first thing to do with pygame lib, init it
pygame.init()

#init variable for the column and row window app
SQUARESIZE = 90
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE# (ROW_COUNT+1) for the player choice space

#init the size of the window app
size = (width, height)
# Radius of the piece
RADIUS = int(SQUARESIZE/2 - 5)
#display screen
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
# Font for screen app
myfont = pygame.font.SysFont("monospace", 75)
# Random select first player
turn = random.randint(PLAYER, AI)
while not game_over:
    # get all input with pygame function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
            # Track wherever is the mouse
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

# ----TODO ADD right/left + enter input 

        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #Ask for palyer 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 win!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                        
                    print_board(board)
                    draw_board(board)
                    
                    turn +=1
                    turn = turn % 2
            
            
    # #Ask for palyer 2 input
    if turn == AI and not game_over:
        
        col, minimax_score = minimax(board, 2, True)
        
        if is_valid_location(board, col):
            pygame.time.wait(1000)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            
            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 win!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            
        
            print_board(board)
            draw_board(board)
            
            turn +=1
            turn = turn % 2
    
    if game_over:
        pygame.time.wait(3000)
    