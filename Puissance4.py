import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0) 

ROW_COUNT = 6
COLUMN_COUNT = 7

#create our board function
def created_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))#our dimensional board, with 0 we have 7 for y, 7+0=8 for x
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

#function check if Player input is valid     
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    #check board position equal 0
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

#change the orientation of the borad = 180°
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
        for r in range(3, ROW_COUNT):#ROW_COUNT-3 because you can't win with 3 power
             if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                 return True
             
# For print board in pygame
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

board = created_board()
#initialize Game loop condition
game_over = False
turn = 0

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

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    # get all input with pygame function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
            # Track wherever is the mouse
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # print(event.pos)
            #Ask for palyer 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 win!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
            
            
            
            # #Ask for palyer 2 input
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
                    
            print_board(board)
            draw_board(board)
            turn +=1
            turn = turn % 2
            
            if game_over:
                pygame.time.wait(3000)
    