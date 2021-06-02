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

        #self.mutation(bestChromosome)       # test

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
                for i in range(100):  # generate several possible final sate playing this move!
                    # generate the rest of the grid many Time !
                    population.append(self.get_sequence(current_game.copy_state(), [x + 1], 4))
        return population

    def fitness(self, chromosome):
        value = 0
        game = self.ai_game.copy_state()
        for move in chromosome:
            game.place(move - 1)
            if game.get_turn() != self.player:  # Ai turn was played
                value += self.move_impact(game, move - 1)
            else:
                value -= self.move_impact(game, move - 1)  # opponent turn was played

        if game.get_win() == self.player:
            value += 1000
        return value

    def selection(self, population):
        selection = PriorityQueue()
        for chromosome in population:
            value = self.fitness2(chromosome)
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
        gain, wining_pos = self.vertical_gain(board, x, y)
        value += gain
        if wining_pos is not None:
            pass

        value += self.horizontal_gain(board, x, y)
        return value

    def vertical_gain(self, board, x, y):
        player = board[x][y]
        gain = 0
        min_row = max(y - 3, 0)
        max_row = min(y + 3, self._rows - 1)
        aligned_coins = 0
        wining_pos = None
        for r in range(y, min_row - 1, -1):
            if board[x][r] == player:
                gain += 1
                aligned_coins += 1
            else:
                break  # there are "aligned_coins" coins all ready align
        if 4 - aligned_coins <= max_row - y:  # it possible to align 4 coins in this column
            gain += 2
        if aligned_coins == 3:
            wining_pos = (x, y + 1)
        return gain, wining_pos

    def horizontal_gain(self, board, x, y):
        player = board[x][y]
        min_col = max(x - 3, 0)
        max_col = min(x + 3, self._cols - 1)
        gain = 0
        aligned_coins = 0
        gap = 0
        winning_pos = []
        for c in range(x, max_col + 1):
            if board[c][y] == player:
                gain += 2
                aligned_coins += 1
            elif board[c][y] == 0:
                gap += 1
                if gap > 1:
                    break
                winning_pos.append(c)
                gain += 1

            else:
                break
        for c in range(x - 1, min_col - 1, -1):
            if board[c][y] == player:
                gain += 2
                aligned_coins += 1
            elif board[c][y] == 0:
                gain += 1
                if board[c + 1][y] == player:
                    winning_pos.append(c)
            else:
                break
        if aligned_coins != 3:
            winning_pos = None
        return gain, winning_pos

    # AMMAR
    def mutation(self, chromosome):
        """ this function exchange two positions of the chromosome
        :param chromosome:
        :return: mutated chromosome
        """
        mutated_chromosome = deepcopy(chromosome)
        maxpos = len(mutated_chromosome)-1
        pos1 = random.randint(0, maxpos)
        pos2 = random.randint(0, maxpos)
        while pos2 == pos1:
            pos2 = random.randint(0, maxpos)
        # print("pos1 exchange : ", pos1)
        # print("pos2 exchange : ", pos2)
        # print("chromo1 : ", mutated_chromosome)
        mutated_chromosome[pos1], mutated_chromosome[pos2] = mutated_chromosome[pos2],mutated_chromosome[pos1]
        # print("chromo2 : ", mutated_chromosome)
        return mutated_chromosome

    def crossover(self, chromosome1, chromosome2):
        pass

    # JC
    def fitness2(self, chromosome):
        value = 0
        val = 0
        game = self.ai_game.copy_state()
        for move in chromosome:
            game.place(move - 1)
            # test = self.prov(game)
            val += self.prov(game)
            """if test > val:
                val = test"""
        return val

    def prov(self, game):
        value = 0
        for i in range(7):
            for j in range(6):
                if i < 3:  # top
                    # print("yop 1")
                    value += self.aligned(game.get_board(), i, j, 1, 0)  # to the top
                    if j < 2:  # right
                        # print("yop 2")
                        value += self.aligned(game.get_board(), i, j, 1, 1)
                if j < 2:  # right
                    # print("yop 3")
                    value += self.aligned(game.get_board(), i, j, 0, 1)
                    if i > 2:  # left
                        # print("yop 4")
                        value += self.aligned(game.get_board(), i, j, -1, 1)
        # print("Value : ", value)
        return value

    def aligned(self, board, coord_x, coord_y, dir_x, dir_y):
        x, y = coord_x, coord_y
        nbr_clr, nbr_empty, i = 0, 0, 0
        color = 0
        value = 0
        while i < 4:
            # print(x,y)
            if color == 0:
                color = board[x][y]
            if board[x][y] == 0:
                nbr_empty += 1
            elif board[x][y] == color:
                nbr_clr += 1
            else:
                value -= 1
                break
            x += dir_x
            y += dir_y
            i += 1
        if nbr_clr + nbr_empty == 4:
            if nbr_clr == 2:
                value = 10
            elif nbr_clr == 3:
                value = 50
            elif nbr_clr == 4:
                value = 1000
        if color == self.adv:
            value *= -10
        return value
