import pygame
from player import player
from alpha_beta import Minimax
import numpy as np

def move(turn, val):

    val = int(val)
    if ( (val > 5) or (val < 0) ):
        print("Invalid move")
        return turn
    curr_player_bins = None
    opp_player_bins = None
    if turn == 0:
        curr_player_bins = player1.bins
        opp_player_bins = player2.bins
    elif turn == 1:
        curr_player_bins = player2.bins
        opp_player_bins = player1.bins
    success = minimax.move_algo(curr_player_bins, opp_player_bins, val)
    if success == 0:
        return 1-turn
    return turn

def get_bin(turn, pos):
    x = pos[0]
    y = pos[1]
    if turn == 0:
        # player 1 's turn
        # incase of clicking outside bins
        if (y < 50) or (y > 150):
            return -1
    elif turn == 1:
        # player 2's turn
        if (y < 150) or (y > 250):
            return -1
    # out of x coordinates
    if (x < 150) or (x > 850):
        return -1
    # relative distance from 0 : 150 - starting coord ; 120 : difference of each x
    rel_bin = int( (x - 150) / 120 )

    if ( x >= player1_bin_coord[rel_bin][0] ) and x <= ( player1_bin_coord[rel_bin][0] + 100 ):
        if turn == 0:
            rel_bin = 5 - rel_bin
        return rel_bin
    else:
        return -1


def result():
    if player1_score > player2_score:
        return "player 1 won the match"
    elif player1_score < player2_score:
        return "player 2 won the match"
    return "tied"





#--------------------------------------------------------------------------#
print("Insert depth")
depth = int( input() )
print("Choose heuristic")
heuristic = int( input() )
minimax = Minimax(depth, heuristic)

pygame.init()

font1 = pygame.font.SysFont('Calibri',24,True,True)

# Set up the drawing window
width, height = 1000, 300
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Mancala")

# draw stone circles
red = (200,0,0)
radius = 10

# initialise players
player1 = player()
player2 = player()

# coordinates
player2_store = [900, 50, 80, 200]
player1_store = [10, 50, 80, 200]
player1_bin_coord = []
player2_bin_coord = []

x_diff = 120
x, y = 150, 50
for i in range(6):
    player1_bin_coord.append([x, y])
    player2_bin_coord.append([x, y + 100])
    x = x + x_diff

# turn - 0 : player 1 , 1: player 2
turn = 0
val = -1
print("If you want to go first, press 1, otherwise press 0")
go = int( input() )
if go == 1:
    turn = 1
# Run until the user asks to quit
running = True
while running:

    # Fill the background with white
    screen.fill((255, 255, 255))


    # Drawing Rectangle
    color = (0, 0, 0)
    if minimax.check_terminal_state(player1.bins[:6]) or minimax.check_terminal_state(player2.bins[:6]):
        player1_score = np.sum(player1.bins)
        player2_score = np.sum(player2.bins)
        print("Player 1 score : " + str(player1_score) )
        print("Player 2 score : " + str(player2_score) )
        # score1 = "Player 1 score : " + str(player1_score)
        # str = font1.render("Player 1 score : " + str(player1_score), 1, (0, 0, 0))
        # screen.blit(str, (300, 100))
        # score2 = "Player 2 score : " + str(player2_score)
        # str = font1.render(score2, 1, (0, 0, 0))
        # screen.blit(str, (400, 150))
        print_result = result()
        end = True
        while end:
            str = font1.render(print_result, 1, (0, 0, 0))
            screen.blit(str, (500, 150))
            # Flip the display
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    end = False

    else:
        turn_str = font1.render("Player " + str(turn + 1) + "'s turn", 1, (0, 0, 0))
        screen.blit(turn_str, (400, 0))

        pygame.draw.rect(screen, color, pygame.Rect(player1_store), 2)
        pygame.draw.rect(screen, color, pygame.Rect(player2_store), 2)
        player1_bin_no = font1.render(str(player1.bins[6]), 1, (0, 0, 0))
        player2_bin_no = font1.render(str(player2.bins[6]), 1, (0, 0, 0))
        screen.blit(player1_bin_no, player1_store[:2])
        screen.blit(player2_bin_no, player2_store[:2])

        for i in range(6):
            player1_bin_no = font1.render(str(player1.bins[5-i]), 1, (0, 0, 0))
            player2_bin_no = font1.render(str(player2.bins[i]), 1, (0, 0, 0))
            screen.blit(player1_bin_no, player1_bin_coord[i])
            screen.blit(player2_bin_no, player2_bin_coord[i])
            p1_bin_no = font1.render(str(6 - i), 1, (0, 0, 0))
            p2_bin_no = font1.render(str(i + 1), 1, (0, 0, 0))
            screen.blit(p1_bin_no, [player1_bin_coord[i][0] + 50, player1_bin_coord[i][1] - 25] )
            screen.blit(p2_bin_no, [player2_bin_coord[i][0] + 50, player2_bin_coord[i][1] + 110] )
            pygame.draw.rect(screen, color, pygame.Rect([player1_bin_coord[i][0], player1_bin_coord[i][1], 100, 100]), 2)
            pygame.draw.rect(screen, color, pygame.Rect([player2_bin_coord[i][0], player2_bin_coord[i][1], 100, 100]), 2)
        if val != -1:
            move_1 = font1.render("Move: " + str(val+1), 1, (0, 0, 0))
            screen.blit(move_1, (600, 0))
        # Flip the display
        pygame.display.flip()

        if turn == 0:
            #
            # move = font1.render("Player 1's move : " + str(val), 1, (0, 0, 0))
            # screen.blit(move, (400, 20))
            # Did the user click the window close button?
            # comment below two lines for userplay
            if val == -1:
                val = minimax.minmax(player1, player2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # val = get_bin(turn, pos)
                    turn = move(turn, val)
                    val = -1


        elif turn == 1:
            # uncomment this for autoplay
            # if val == -1:
            #     val = minimax.minmax(player2, player1)
            for event in pygame.event.get():
                # Did the user click the window close button?
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # comment below two lines for autoplay
                    val = get_bin(turn, pos)
                    turn = move(turn, val)
                    # uncomment below two lines for userplay
                    # if val != -1:
                    #     turn = move(turn, val)
                    val = -1


# Done! Time to quit.
pygame.quit()
