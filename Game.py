import pygame
from pygame.locals import *
import sys
import numpy as np
from Board import *
from Agent import RandAgent, MinimaxAgent

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = 960, 720
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
GOLD = pygame.Color(255, 255, 0)
BLUE = pygame.Color(0, 0, 255)
LIGHT_BLUE = pygame.Color(100, 100, 255)
GREY = pygame.Color(127, 127, 127)

counter_sound = pygame.mixer.Sound("counter.ogg")
counter_sound.set_volume(0.1)

window = pygame.display.set_mode(SCREEN_SIZE)

w, h = 8, 8
board = Board(h, w)

depth = 4
agent = MinimaxAgent(board, depth)

def draw_board(surface, board, back_colour, empty_colour, counter1_colour, counter2_colour, rect):
    x, y, width, height = rect
    board_arr = board.get_board()
    board_height, board_width = board_arr.shape

    pygame.draw.rect(surface, back_colour, rect)

    diameter = int(np.min([(1 / board_width) * width, (1 / board_height) * height]))
    radius = diameter // 2
    for i in range(board_width):
        for j in range(board_height):
            v = board_arr[j, i]
            if v == 0:
                colour = empty_colour
            elif v == PIECE1:
                colour = counter1_colour
            elif v == PIECE2:
                colour = counter2_colour
                
            xpos = x + int((i / board_width) * width + radius)
            ypos = y + int((j / board_height) * height + radius)
            pygame.draw.circle(surface, colour, (xpos, ypos), radius)

    winner = board.get_winner()
    if winner != NO_PIECE:
        outline_width = np.min([width, height]) // 64
        
        if winner == PIECE1:
            colour = counter1_colour
        elif winner == PIECE2:
            colour = counter2_colour
        elif winner == STALEMATE:
            colour = GREY
            
        pygame.draw.rect(surface, colour, rect, outline_width)

    # Return a list of rects, one for each column
    x_coords = [x + int((i / board_width) * width) for i in range(board_width)]
    rects = [pygame.Rect(a, y, diameter, height) for a in x_coords]

    return rects

    

    

do_loop = True
do_update = True
selected_column = -1
board_rects = []
while do_loop:
    
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == QUIT:
            # Exit when close button is pressed
            do_loop = False

        elif event.type == MOUSEMOTION:
            # Check if the mouse is in any of the columns
            flag = False
            for r in range(len(board_rects)):
                if board_rects[r].collidepoint(event.pos):
                    selected_column = r
                    flag = True
                    do_update = True
            if not flag:
                selected_column= -1

        elif event.type == MOUSEBUTTONDOWN:
            # If a column is selected and nobody has won, play this column
            if selected_column != -1 and board.get_turn() == PIECE1:
                # Try placing in this column
                try:
                    res = board.play(selected_column)
                    counter_sound.play()
                except:
                    # Todo: play a sound on failure
                    pass
                do_update = True

        elif event.type == KEYDOWN:
            # Reset the board and start a new game
            if event.key == K_r:
                board = Board(h, w)
                agent = MinimaxAgent(board, depth)
                do_update = True
            # Exit
            if event.key == K_ESCAPE:
                do_loop = False

    turn = board.get_turn()
    if turn == PIECE2:
        move = agent.get_move()
        board.play(move)
    
    if do_update:
        window.fill(BLACK)
        board_rects=draw_board(window, board, LIGHT_BLUE, WHITE, BLUE, RED, (16, 16, SCREEN_WIDTH-32, SCREEN_HEIGHT-32))

        if selected_column != -1:
            pygame.draw.rect(window, GOLD, board_rects[selected_column], 4)
        
        pygame.display.update()
        do_update = False


pygame.quit()
sys.exit()
