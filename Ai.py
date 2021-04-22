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
        self.weights = [[3, 4, 12, 12, 4, 3], [4, 6, 8, 8, 6, 4], [5, 8, 11, 11, 8, 5], [7, 10, 13, 13, 10, 7],
                        [5, 8, 11, 11, 8, 5],
                        [4, 6, 8, 8, 6, 4], [3, 4, 5, 5, 4, 3]]
        self._cols = None
        self._rows = None

    def random_play(self, game):

        return self.ai_play(game)

    def ai_play(self, game):
        self.init_game = game
        self._cols = game.get_cols()
        self._rows = game.get_rows()
        games = self.gen_sol(game)
        sample = len(games) // 100
        print("Generation: ", sample)
        generation0 = self.selection(games, sample)  # the first generation of solutions!
        # loop until min fitness value achieve or max generation
        final_game = generation0[0][1]
        print(final_game.get_board())
        print("game fitness = ", generation0[0][0])

        legal_moves = self.extract_possible_moves(generation0[0])  # extracting the move that can lead to the best sol
        best_move = self.find_best_move(legal_moves, generation0[0][1])  # best move from legal_moves
        print(best_move[0])
        move = best_move[1]
        print(move)
        return move[0]

    def gen_sol(self, game):
        solutions = []
        for x in range(7):  # playing the seven possible moves
            current_game = deepcopy(game)
            if current_game.place(x) is not None:
                for i in range(100):  # generate several possible final sate playing this move!
                    # generate the rest of the grid many Time !
                    solutions.append(self.complete_game(deepcopy(current_game)))  # can use only one deepcopy
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
        value += self.pawns_weight(game.get_board())
        if game.get_win() == self.player:
            value += 1000
            factor = (42 - self.get_nbr_pawn(game.get_board()))*10
            value += factor
        elif game.get_win() == 0:
            value += 20
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

    def get_nbr_pawn(self, board):
        nbr = 0
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == self.player:
                    nbr += 1
        return nbr

    def get_valid_moves(self):
        valid_moves = []
        board = self.init_game.get_board()
        for x in range(len(board)):
            if min(board[x]) == 0:
                for y in range(len(board[x])):
                    if board[x][y] == 0:
                        pos = y
                        break
                valid_moves.append([x, y])
        return valid_moves

    def extract_possible_moves(self, best_game):
        best_board = best_game[1].get_board()
        valid_moves = self.get_valid_moves()
        possible_moves = []
        for move in valid_moves:
            if best_board[move[0]][move[1]] == self.player or best_board[move[0]][move[1]] == 0:
                possible_moves.append(move)
        return possible_moves

    def find_best_move(self, possible_moves, best_game):
        available_moves = []
        current_board = self.init_game.get_board()
        best_board = best_game.get_board()
        for move in possible_moves:
            value = 0
            best_value = best_board[move[0]][move[1]]  # can be 0 or player !
            current_board[move[0]][move[1]] = self.player
            if self.init_game.check_win(move) == self.player:
                value += 1000
            elif best_value == self.player:  # casual play but playing to achieve the best state
                value += 10
                value += self.weights[move[0]][move[1]]
            current_board[move[0]][move[1]] = self.adv
            if self.init_game.check_win(move) == self.adv:
                value += 100
            available_moves.append([value, move])
            current_board[move[0]][move[1]] = 0
            # self.init_game.check_win(move)

        return max(available_moves)

    def pawns_weight(self, board):                      # merge with get pawn number!
        value = 0
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == self.player:
                    value += self.weights[x][y]
                elif board[x][y] == self.adv:
                    value -= (self.check1([x, y], board))*5
                    pass

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
            if count == 3:                              # check for alignment of 3 adv coins
                value += 1

        # Vertical check
        count = 0
        for ri in range(min_row, max_row + 1):
            if board[c][ri] == self.adv:
                count += 1
            else:
                count = 0
            if count == 4:
                value += 1

        count1 = 0
        count2 = 0
        # Diagonal check
        return value
