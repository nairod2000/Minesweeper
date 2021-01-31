from tile import Tile
from random import sample
import os

class Minesweeper:
    def __init__(self, rows=16, cols=30, bombs=99, human_player=True):
        self.rows = rows
        self.cols = cols
        self.total_tiles = rows * cols
        self.bombs = bombs
        self.bomb_cords = self.generate_bomb_locations()
        # initalize real board
        self.board = self._init_board_r()

        self.lost_game = False
        self.human_player = human_player

    def generate_bomb_locations(self):
        idxs = sample(range(self.total_tiles), self.bombs)
        cord_list = list()
        for idx in idxs:
            row = idx // self.cols
            col = idx % self.cols
            cord_list.append((row, col))

        return cord_list


    def _init_board_r(self):

        board = [[Tile(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self._populate_bombs(board)
        self._find_neighbors(board)
        self._set_display(board)
        return board

    def _populate_bombs(self, board):
        # should set __getitem__()
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.bomb_cords:
                    board[row][col].is_bomb = True

    def _find_neighbors(self, board):
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = 0

                idxs_to_check = [(row-1, col-1), (row-1, col), (row-1, col+1), (row, col-1), (row, col+1), (row+1, col-1), (row+1, col), (row+1, col+1)]
                # check above
                for idx in idxs_to_check:
                    _row, _col = idx
                    if not (0 <= _row < self.rows) or not (0 <= _col < self.cols):
                        continue
                    
                    try:
                        if board[_row][_col].is_bomb:
                            neighbors += 1
                    except IndexError:
                        print(f"{_row} {_col}")
                        quit()
                
                board[row][col].neighbors = neighbors


    def _set_display(self, board):
        # return a board of display tiles
        for row in range(self.rows):
            for col in range(self.cols):
                board[row][col].is_display = True

        return board

    def __repr__(self):
        print("\033c")
        return str(self)
        
    def __str__(self):
        display_str = ""
        for i in range(16):
            display_str += (str(self.board[i]) + "\n")
        return display_str

    def make_move(self, row, col):
        self.board[row][col].is_clicked = True
        
        if self.board[row][col].is_bomb:
            self.lost_game = True
            if self.human_player:
                print('Game over.')
        elif self.human_player:
            if self.board[row][col].neighbors == 0:
                self.clear_path(self.board[row][col])

    def clear_path(self, tile):
        
        tiles_to_check = [tile]

        for tile in tiles_to_check:        

            surrounding_tiles = [(tile.row-1, tile.col-1), (tile.row-1, tile.col), (tile.row-1, tile.col+1), (tile.row, tile.col-1), (tile.row, tile.col+1), (tile.row+1, tile.col-1), (tile.row+1, tile.col), (tile.row+1, tile.col+1)]

            for pos in surrounding_tiles:
                
                _row, _col = pos

                if not (0 <= _row < self.rows) or not (0 <= _col < self.cols):
                    continue

                print(f"{_row} {_col}")

                if not self.board[_row][_col].is_bomb:
                    self.board[_row][_col].is_clicked = True
                    if self.board[_row][_col].neighbors == 0 and not self.board[_row][_col] in tiles_to_check:
                        tiles_to_check.append(self.board[_row][_col])
            

if __name__ == "__main__":
    m = Minesweeper()
    while not m.lost_game:
        print(m)
        user_input = input("enter corrdinates: ")
        row, col = int(user_input[0]), int(user_input[2])
        m.make_move(row, col)
