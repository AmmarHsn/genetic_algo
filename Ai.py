import random
from copy import deepcopy
from queue import PriorityQueue


class Ai:
    def __init__(self, player):
        """ AI PLAYER CLASS """
        self.player = player
        if player == 1:  # can do better
            self.adv = 2
        else:
            self.adv = 1
        self.init_game = None
        self.weights = [[3, 4, 5, 5, 4, 3], [4, 6, 8, 8, 6, 4], [11, 8, 11, 11, 8, 5], [12, 10, 13, 13, 10, 7],
                        [11, 8, 11, 11, 8, 5],
                        [4, 6, 8, 8, 6, 4], [3, 4, 5, 5, 4, 3]]
        self._cols = None
        self._rows = None

    def random_play(self, game):

        return self.ai_play(game)

    def ai_play(self, game):
        self.init_game = game
        self._cols = game.get_cols()
        self._rows = game.get_rows()

        # creation generations of solutions
        counter = 0
        best_games = PriorityQueue()

        for i in range(4):
            games = self.gen_sol(game)                  # Generation
            sample = len(games) // 10
            generation = self.selection(games, sample)  # sampling of best solutions!
            gen_best_game = generation[0]               # the best sol of the generation
            best_games.put([gen_best_game[0], counter, gen_best_game[1]])   # saving result
            counter += 1
            print("Generation ", i, " = ", gen_best_game[0] * -1)

        final_game = best_games.get()
        print("All Gen best = ", final_game[0] * -1)
        # loop until min fitness value achieve or max generation
        print(final_game[2][1].get_board())
        return final_game[2][0]

    def gen_sol(self, game):
        solutions = []
        for x in range(7):  # playing the seven possible moves
            current_game = deepcopy(game)
            if current_game.place(x) is not None:
                for i in range(100):  # generate several possible final sate playing this move!
                    # generate the rest of the grid many Time !
                    solutions.append([x, self.complete_game(deepcopy(current_game))])  # can use only one deepcopy
        return solutions

    def complete_game(self, game):
        while game.get_win() is None:
            played = False
            # maxcol = game.get_cols
            while not played:
                if game.place(random.randint(0, 6)):  # it can loop
                    played = True
        return game

    def fitness(self, game):
        value = 0
        # Board qualification
        value += self.pawns_weight(game[1].get_board())
        if game[1].get_win() == self.player:
            value += 1000
            value += self.first_row_check(game[1].get_board())
        elif game[1].get_win() == 0:
            value += 20

        # move qualification
        value += self.move_impact(game[0])
        return value

    def selection(self, games, population_nbr):
        population = PriorityQueue()
        counter = 0
        for elem in games:
            value = self.fitness(elem)
            population.put([-value, counter, elem])  # adding a minus to use PriorityQueue
            counter += 1
        best_of_pop = []
        for i in range(population_nbr):
            individual = population.get()
            best_of_pop.append([individual[0], individual[2]])
        return best_of_pop

    def move_impact(self, move):
        value = 0
        future_game = deepcopy(self.init_game)
        c0, r0 = future_game.place(move)  # playing the move !
        winner = future_game.get_win()
        if winner == self.player:  # wining case
            return 10000
        # winner == 0  draw case
        value += 20
        next_move = future_game.place(move)  # playing for adversary one step further
        winner_in_2step = future_game.get_win()

        if next_move is not None:
            if winner_in_2step == self.adv:
                value -= 100                         # adversary will win after my move
            else:
                value += 10                         # no one is wining
            # coming back from the future
            future_game.get_board()[c0][r0+1] = 0
        future_game.get_board()[c0][r0] = 0
        future_game._won = 0
        future_game._turn = self.adv
        future_game.place(move)                 # if adversary plays first the move
        winner2 = future_game.get_win()
        if winner2 == self.adv:
            value += 1000
        elif future_game.place(move) is not None:    # going one step further to chek if we win !
            if future_game.get_win == self.player:
                value -= 30                          # waiting to the adversary to play first
        return value

    def pawns_weight(self, board):  # merge with get pawn number!
        value = 0
        my_pawns = 0
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == self.player:
                    value += self.weights[x][y]
                    my_pawns += 1
                elif board[x][y] == self.adv:
                    value -= (self.check1([x, y], board)) * 5
        value += 64 - my_pawns
        return value

    def check1(self, pos, board):
        c = pos[0]
        r = pos[1]
        min_col = max(c - 2, 0)
        max_col = min(c + 2, self._cols - 1)
        min_row = max(r - 2, 0)
        max_row = min(r + 2, self._rows - 1)

        value = 0

        # Horizontal check
        count = 0
        for ci in range(min_col, max_col + 1):
            if board[ci][r] == self.adv:
                count += 1
            else:
                count = 0
            if count == 3:  # check for alignment of 3 adv coins
                value += 1

        # Vertical check
        count = 0
        for ri in range(min_row, max_row + 1):
            if board[c][ri] == self.adv:
                count += 1
            else:
                count = 0
            if count == 3:
                value += 1

        count1 = 0
        count2 = 0
        # Diagonal check
        return value

    def first_row_check(self, board):
        value = 0
        for col in range(2, 5):
            if board[col][0] != self.player:
                value -= 30
        return value
