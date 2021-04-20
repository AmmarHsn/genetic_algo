import random
from copy import deepcopy


class Ai:
    def __init__(self, player):
        """ AI PLAYER CLASS """
        self.player = player
        if player == 1:  # can do better
            self.adv = 2
        else:
            self.adv = 1
        self.init_game = None

    def random_play(self, game):

        return self.ai_play(game)

    def ai_play(self, game):
        self.init_game = game
        games = self.gen_sol(game)
        sol = self.selection(games)  # we have on final game the best one
        g = sol[1]
        b = g.get_board()
        print(b)

        legal_moves = self.extract_possible_moves(sol)  # extracting the move that can lead to the best sol
        best_move = self.find_best_move(legal_moves, sol[1])  # best move from legal_moves
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
        if game.get_win() == self.player:
            value += 1000
            factor = self.get_nbr_pawn(game.get_board())
            value += (42 - factor) * 10
        elif game.get_win() == 0:
            value += 20
        return value

    def selection(self, games):
        best_sol = []
        max_value = 0
        for elem in games:
            value = self.fitness(elem)
            if max_value < value:
                max_value = value
            best_sol.append([value, elem])
        for sol in best_sol:  # to be modify
            if sol[0] == max_value:
                return sol
        # return max(best_sol)

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
            current_board[move[0]][move[1]] = self.adv
            if self.init_game.check_win(move) == self.adv:
                value += 100
            available_moves.append([value, move])
            current_board[move[0]][move[1]] = 0
            # self.init_game.check_win(move)

        return max(available_moves)
