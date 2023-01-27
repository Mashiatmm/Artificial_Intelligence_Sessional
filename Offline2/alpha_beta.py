import sys
import numpy as np
from player import player

class Minimax:
    def __init__(self, depth, heuristic):
        self.max_depth = depth
        self.heuristic = self.set_heuristic(heuristic)
        self.add_moves = 0
        self.move_order = [0, 1, 2, 3, 4, 5]

    def set_heuristic(self, heuristic):
        if heuristic == 1:
            return self.h1
        elif heuristic == 2:
            return self.h2
        elif heuristic == 3:
            return self.h3
        return self.h1

    def set_move_order(self, order):
        self.move_order = order

    def check_terminal_state(self, p1_bins):
        return ( np.sum(p1_bins) == 0 )

    def minmax(self, p1, p2):
        '''
        Args:
             p : player
        '''
        # # print(self.max_depth)
        self.add_moves = 0
        alpha = -1 * sys.maxsize
        beta = 1 * sys.maxsize
        idx, max_val = self.max_value(p1.bins.copy(), p2.bins.copy(), 0, alpha, beta)
        return idx

    def max_value(self, p1_bins, p2_bins, depth, alpha, beta):
        '''
            p1_bins : player's bins
            p2_bins : opponent's bins
        '''
        # print("max depth: " + str(depth) )
        if depth == self.max_depth or self.check_terminal_state(p1_bins[:6]):
            return -1, self.heuristic(p1_bins, p2_bins)
        max_val = -1*sys.maxsize
        idx = -1
        for i in self.move_order:
            temp_p1 = p1_bins.copy()
            temp_p2 = p2_bins.copy()
            success = self.move_algo(temp_p1, temp_p2, i)
            # print("Max func")
            # print("success " + str(success) )
            # print(temp_p1, temp_p2)
            val = 0
            if success == 0:
                index, val = self.min_value(temp_p2, temp_p1, depth + 1, alpha, beta)
            elif success == 1:
                index, val = self.max_value(temp_p1, temp_p2, depth, alpha, beta)
                self.add_moves += 1
            else:
                continue
            # beta pruning, if val > beta, return
            if val >= beta:
                # print("Beta pruned")
                return index, val
            if val > max_val:
                max_val = val
                idx = i
            alpha = max(alpha, val)
            # # print(str(i) + " : " + str(val) + " : depth : " + str(depth) )
            # print("beta : " + str(beta) )
        return idx, max_val

    def min_value(self, p1_bins, p2_bins, depth, alpha, beta):
        '''
        :param p1_bins: opponent's bins
        :param p2_bins: player's bins
        '''
        # # print("Min func")
        # # print("min depth " + str(depth) )
        if depth == self.max_depth or self.check_terminal_state(p1_bins[:6]):
            # # print(h1(p2_bins, p1_bins))
            return -1, self.heuristic(p2_bins, p1_bins)
        min_val = sys.maxsize
        idx = -1
        for i in self.move_order:
            # print("Min func")
            temp_p1 = p1_bins.copy()
            temp_p2 = p2_bins.copy()
            success = self.move_algo(temp_p1, temp_p2, i)
            # print("success " + str(success))
            # print(temp_p1, temp_p2)
            val = 0
            if success == 0:
                index, val = self.max_value(temp_p2, temp_p1, depth + 1, alpha, beta)
            elif success == 1:
                index, val = self.min_value(temp_p1, temp_p2, depth, alpha, beta)
            else:
                continue
            # alpha beta pruning. check if min value is less than alpha, then go back
            if val <= alpha:
                # print("alpha pruned")
                return index, val
            if val < min_val:
                min_val = val
                idx = i
            beta = min(beta, val)
            # print("alpha : " + str(alpha) )
        return i, min_val

    def move_algo(self,p1_bins, p2_bins, bin_no):
        '''
        :param p1_bins: player's bins
        :param p2_bins: opponent's bins
        :param bin_no: bin_index where the player will give his next move
        :return:
            -1 : invalid move, terminal state
            0 : successful
            1 : additional move
        '''
        stone_no = p1_bins[bin_no]
        if stone_no == 0:
            # invalid move
            return -1
        p1_bins[bin_no] = 0
        start_bin = bin_no + 1
        while stone_no != 0:
            for j in range(start_bin, 7):
                p1_bins[j] = p1_bins[j] + 1
                if stone_no == 1:
                    if j == 6:
                        # last one in player's store, get a free turn
                        return 1
                    elif p1_bins[j] == 1:
                        # get the opponent's stones of the opposite side
                        p1_bins[6] = p1_bins[6] + p2_bins[5-j]
                        p2_bins[5-j] = 0
                    # break as last one
                    stone_no -= 1
                    break

                stone_no -= 1

            # opponent's bin
            if stone_no != 0:
                for j in range(6):
                    p2_bins[j] = p2_bins[j] + 1
                    stone_no -= 1
                    if stone_no == 0:
                        break
            start_bin = 0

        return 0


    def h1(self, p1_bins, p2_bins):
        '''
        heuristic function : (stones_in_my_storage – stones_in_opponents_storage)
        :param p1_bins: player's bins
        :param p2_bins: opponent's bins
        :return: heuristic value
        '''
        # # print("h1")
        # # print(p1_bins)
        # # print(p2_bins)
        return p1_bins[6]-p2_bins[6]

    def h2(self, p1_bins, p2_bins):
        '''
        heuristic function : W1 * (stones_in_my_storage – stones_in_opponents_storage) + W2 * (stones_on_my_side – stones_on_opponents_side)
        :param p1_bins: player's bins
        :param p2_bins: opponent's bins
        :return: heuristic value
        '''
        return 2 * self.h1(p1_bins, p2_bins) + 1 * (np.sum(p1_bins[:6]) + np.sum(p2_bins[:6]))

    def h3(self, p1_bins, p2_bins):
        '''
        heuristic function : W1 * (stones_in_my_storage – stones_in_opponents_storage) + W2 * (stones_on_my_side – stones_on_opponents_side)
                            + W3 * additional_moves_earned
        :param p1_bins: player's bins
        :param p2_bins: opponent's bins
        :return: heuristic value
        '''
        return 1 * self.h2(p1_bins, p2_bins) + 2 * self.add_moves

    def h4(self, p1_bins, p2_bins):
        '''
        heuristic function : W1 * h3 + W2 * ( how_close_I_am_to_winning - how_close_opp_is_to_winning )
        :param p1_bins:
        :param p2_bins:
        :return:
        '''
        win_chance = int( p1_bins[6] / 24 )
        lose_chance = int( p2_bins[6] / 24 )
        return 1.5 * self.h3(p1_bins, p2_bins) + 3 * (win_chance - lose_chance)

    def h5(self, p1_bins, p2_bins):
        '''
        heuristic function : W1 * h4 + W2 * ( #_of_stones_close_to_my_storage - #_of_stones_close_to_opponents_storage )
        :param p1_bins:
        :param p2_bins:
        :return:
        '''
        player_close = 0
        opp_close = 0
        for i in range(6):
            if p1_bins[i] >= i + 1 :
                player_close += i + 1
            else:
                player_close += p1_bins[i]
            if p2_bins[i] >= i + 1 :
                opp_close += i + 1
            else:
                opp_close += p2_bins[i]

        return 1 * self.h4(p1_bins, p2_bins) + 1.5 * (player_close - opp_close)

    def h6(self, p1_bins, p2_bins):
        '''
        heuristic function : W1 * h5 + W2 * first_valid_move
        :param p1_bins:
        :param p2_bins:
        :return:
        '''
        valid_move = -1
        for i in range(5, -1, -1):
            if p1_bins[i] > 0 :
                valid_move = i
                break
        return 1 * self.h5(p1_bins, p2_bins) + 2 * valid_move



player1 = player()
player2 = player()

import time

# start = time.time()
# minimax = Minimax(3, 1)
# print("Minimax : " + str(minimax.minmax(player1, player2)) )
# end = time.time()
# print(end - start)
# minimax = Minimax(6, 1)
# print("Minimax : " + str(minimax.minmax(player1, player2)) )