import random

import numpy as np
from copy import deepcopy
from queue import PriorityQueue


class Ai2:
    def __init__(self, player, game):
        """ The new version of AI PLAYER CLASS """
        self.player = player
        if player == 1:  # can do better
            self.adv = 2
        else:
            self.adv = 1
        # self.played_sequence = np.zeros(42, dtype=int)
        self.played_sequence = []
        self.ai_game = game
        self._cols = game.get_cols()
        self._rows = game.get_rows()

    def random_play(self, game):
        move = random.randint(0, 6)
        while game.place(move) is None:
            move = random.randint(0, 6)
        return move

    def ai_play(self, game):
        self.complete_sequence(game)
        print('sequence  = ')
        print(self.played_sequence)

        population = self.generate_population(game)
        bestmove = self.selection(population)
        bestChromosome = bestmove[1]
        fitnessvalue = bestmove[0]

        print("Best sequence :")
        print(bestChromosome)
        print(fitnessvalue)

        move = bestChromosome[0]
        game.place(move - 1)
        self.complete_sequence(game)

        print('sequence  = ')
        print(self.played_sequence)
        return move - 1

    def get_played_move(self, game):  # can do better
        move = None
        for x in range(self._cols):
            for y in range(self._rows):
                if self.ai_game.board_at(x, y) != game.board_at(x, y):
                    move = x
                    return move
        return move

    def complete_sequence(self, game):
        move = self.get_played_move(game)
        self.ai_game.place(move)
        self.played_sequence.append(move + 1)

    def get_sequence(self, game_copy, chromosome, depth):
        turn_counter = 0
        while game_copy.get_win() is None and turn_counter < depth:
            move = random.randint(0, 6)
            while game_copy.place(move) is None:
                move = random.randint(0, 6)
            chromosome.append(move + 1)
            # self.add_move(chromosome_copy, move)
            turn_counter += 1
        return chromosome

    def generate_population(self, game):
        population = []
        for x in range(7):  # playing the seven possible moves
            current_game = game.copy_state()
            if current_game.place(x) is not None:
                for i in range(2):  # generate several possible final sate playing this move!
                    # generate the rest of the grid many Time !
                    population.append(self.get_sequence(current_game.copy_state(), [x+1], 45))
        return population

    def fitness(self, chromosome):
        value = 0
        game = self.ai_game.copy_state()
        for move in chromosome:
            game.place(move-1)
            if game.get_turn() != self.player:     # Ai turn was played
                value += self.move_impact(game, move-1)
            else:
                value -= self.move_impact(game, move-1)     # opponent turn was played

        if game.get_win() == self.player:
            value += 1000
        return value

    def selection(self, population):
        selection = PriorityQueue()
        for chromosome in population:
            value = self.fitness(chromosome)
            selection.put([-value, chromosome])
        return selection.get()

    def move_impact(self, game, move):
        x = move
        board = game.get_board()
        y = 0
        while game.board_at(x, y) != 0 and y < self._rows - 1:
            y += 1
        # checking the position (x, y)
        value = 0
        value += self.vertical_gain(board, x, y)
        value += self.horizontal_gain(board, x, y)
        return value

    def vertical_gain(self, board, x, y):
        player = board[x][y]
        gain = 0
        min_row = max(y - 3, 0)
        max_row = min(y + 3, self._rows - 1)
        for r in range(y, min_row-1, -1):
            if board[x][r] == player:
                gain += 1
            else:
                break                       # there are "gain" coins all ready align
        if 4 - gain <= max_row - y:         # it possible to align 4 coins in this column
            gain += 2
        return gain

    def horizontal_gain(self, board, x, y):
        player = board[x][y]
        min_col = max(x - 3, 0)
        max_col = min(x + 3, self._cols - 1)
        gain = 0
        aligned_coins = 0
        for c in range(x, max_col+1):
            if board[c][y] == player:
                gain += 2
                aligned_coins += 1
            elif board[c][y] == 0:
                gain += 1
            else:
                break
        if 4 - aligned_coins <= x - min_col:         # it possible to align 4 coins horizontally
            gain += 2
        # continue cases
        return gain
