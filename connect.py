import os
import pygame

class Board:
    def __init__(self):
        self.num_cols = 7
        self.num_rows = 6
        self.board = []
        self.construct_board()
        self.display()

    def construct_board(self):
        for row_num in range(self.num_rows):
            row = ['o'] * self.num_cols
            self.board.append(row)

    def display(self):
        os.system('clear')
        for row in self.board:
            print(' '.join(row))
        print()

    def add_piece(self, piece, col):
        if self.is_col_full(col):
            print("You can't add a piece here!")
        else:
            row = self.get_next_valid_row(col)
            self.board[row][col] = piece

    def get_next_valid_row(self, col):
        column = self.get_column(col)
        for row in range(self.num_rows):
            if row + 1 == self.num_rows:  # check if next row is the last one
                break  # if you break here, it returns outside of the loop
            if column[row + 1] != 'o':
                return row
        return self.num_rows - 1  # return last position

    def is_col_full(self, col):
        return 'o' not in self.get_column(col)

    def get_column(self, col):
        transposed = list(map(list, zip(*self.board)))
        return transposed[col]

    def transpose_board(self):
        return


class Game:
    def __init__(self):
        self.turn = 0
        self.board = Board()

        col = ''
        while True:
            piece = 'z' if self.turn % 2 else 'x'
            col = input(f'What column would you like to add {piece} to?\n')
            if col == 'stop':
                break
            self.board.add_piece(piece, int(col) - 1)
            self.board.display()
            self.turn += 1


game = Game()