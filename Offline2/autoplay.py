from player import player
from alpha_beta import Minimax
import numpy as np
import csv

def move(turn, val):
    val = int(val)
    curr_player_bins = None
    opp_player_bins = None
    if turn == 0:
        curr_player_bins = player1.bins
        opp_player_bins = player2.bins
    elif turn == 1:
        curr_player_bins = player2.bins
        opp_player_bins = player1.bins
    success = minmax1.move_algo(curr_player_bins, opp_player_bins, val)
    if success == 0:
        return 1-turn
    return turn

# open the file in the write mode
f = open('comparison.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerow(["Heuristic Name", "Heuristic Name", "Win ", "Lose", "Tie"])


for i in range(1, 7):
    for j in range(i, 7):
        # loop through all heuristics
        depth = 2
        win = 0
        tie = 0
        for num in range(100):
            print(num)
            if num % 20 == 0:
                depth = depth + 1

            player1 = player()
            player2 = player()
            minmax1 = Minimax(depth, i)
            minmax2 = Minimax(depth, j)

            # generate random move_order
            minmax1.set_move_order( np.random.permutation(6) )
            minmax2.set_move_order( np.random.permutation(6) )

            running = True
            turn = 0
            while running:
                if minmax1.check_terminal_state(player1.bins[:6]) or minmax2.check_terminal_state(player2.bins[:6]):
                    player1_score = np.sum(player1.bins)
                    player2_score = np.sum(player2.bins)
                    if player1_score > player2_score:
                        win += 1
                    elif player1_score == player2_score:
                        tie += 1
                    running = False
                if turn == 0 :
                    val = minmax1.minmax(player1, player2)
                elif turn == 1:
                    val = minmax2.minmax(player2, player1)
                turn = move(turn, val)

        # print
        print(" Heuristic " + str(i) + " VS Heuristic " + str(j))
        print("h" + str(i) + " Win : " + str(win) )
        print("h" + str(j) + " Win : " + str(100 - win - tie) )
        print("Tie : " + str(tie) )
        writer.writerow([ "h" + str(i), "h" + str(j), str(win), str(100 - win - tie), str(tie) ])

f.close()