import numpy as np

from player import Player


class AlphaBetaPlayer(Player):
    def __init__(self, player_number, board, depth=3):
        super().__init__(player_number, board)
        self.depth = depth

    def get_next_move(self):
        # TODO: Implement this function based on the minimax algorithm
        best_move = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        # if self.player_number:
        #     best_score = float("inf")
        range_n = 0, self.board.get_n()
        step = 1
        if self.player_number == 0:
            range_n = self.board.get_n() - 1, -1
            step = -1
        for i in range(range_n[0], range_n[1], step):
            for j in range(range_n[0], range_n[1], step):
                if self.board.get_board_grid()[i][j] == self.player_number:
                    for direction in self.board.get_possible_directions(self.player_number):
                        move = (i, j), (i + direction[0], j + direction[1])
                        self.board.start_imagination()
                        if self.board.is_move_valid(self.board.get_imaginary_board(), move, self.player_number):
                            self.board.place_piece_imaginary(move, self.player_number)
                            score = self.minimax(self.depth, not self.player_number, alpha, beta)
                            if score > best_score:
                                best_score = score
                                best_move = move
        return best_move

    def minimax(self, depth, player_number, alpha, beta):
        if depth == 0 or self.board.is_game_over(self.board.get_imaginary_board()):
            return self.get_score()
        range_n = 0, self.board.get_n()
        step = 1
        if player_number == 0:
            range_n = self.board.get_n() - 1, -1
            step = -1
        best_score = float("-inf")
        if player_number:
            best_score = float("inf")
        for i in range(range_n[0], range_n[1], step):
            for j in range(range_n[0], range_n[1], step):
                if self.board.get_imaginary_board()[i][j] == player_number:
                    for direction in self.board.get_possible_directions(player_number):
                        move = (i, j), (i + direction[0], j + direction[1])
                        new_board = np.copy(self.board.get_imaginary_board())
                        if self.board.is_move_valid(self.board.get_imaginary_board(), move, player_number):
                            self.board.place_piece_imaginary(move, player_number)
                        score = self.minimax(depth - 1, not player_number, alpha, beta)
                        if player_number == self.player_number:
                            if score > best_score:
                                best_score = score
                            if best_score >= beta:
                                return best_score
                            alpha = max(alpha, best_score)
                        else:
                            if score < best_score:
                                best_score = score
                            if best_score <= alpha:
                                return best_score
                            beta = min(beta, best_score)
                        self.board.imaginary_board_grid = np.copy(new_board)
        return best_score

    def get_score(self):
        score = (self.board.get_scores(self.board.get_imaginary_board())[self.player_number] -
                self.board.get_scores(self.board.get_imaginary_board())[self.opponent_number])
        for row in range(self.board.get_n()):
            for col in range(self.board.get_n()):
                if self.board.get_imaginary_board()[row][col] == self.player_number:
                    for direction in self.board.get_possible_directions(self.player_number)[1:]:
                        if self.is_coordinate_valid(row + direction[0], col + direction[1]):
                            if self.board.get_imaginary_board()[row + direction[0]][col + direction[1]] == self.opponent_number:
                                score -= 5

        return score

    def is_coordinate_valid(self, row, col):
        return row >= 0 and row < self.board.get_n() and col >= 0 and col < self.board.get_n()