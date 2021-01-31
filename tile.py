class Tile:
    def __init__(self, row, col, neighbors=None, is_bomb=False, is_display=False):
        self.neighbors: int = neighbors
        self.is_bomb: bool = is_bomb
        self.is_clicked: bool = False
        self.row = row
        self.col = col

    def __repr__(self):
        if not self.is_clicked:
            # unclicked
            return "U"
        elif self.is_bomb:
            # bomb
            return "B"
        else:
            return str(self.neighbors)

    def __str__(self):
        if not self.is_clicked:
            return "U"
        elif self.is_bomb:
            return "B"
        else:
            return str(self.neighbors)
