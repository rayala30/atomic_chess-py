# Author: Rafael Ayala
# GitHub username: rayala30
# Date: 5/25/24
# Description: Chessboard Pieces


# CHESS PIECE CLASSES
class Piece:
    """Creates base Piece object that specific chess pieces inherit from"""
    def __init__(self, color):
        self._color = color

    def __str__(self):
        raise ExecutionError("Subclass must implement __str__ method.")

    def move(self):
        raise ExecutionError("Subclass must implement the move method.")

    def get_color(self):
        return self._color


class Pawn(Piece):
    "Creates a Pawn"
    def __init__(self, color):
        super().__init__(color)
        self._has_moved = False

    # This is what will be called by the str('Piece Type') call
    def __str__(self):
        return 'WP' if self._color == 'WHITE' else 'BP'

    def has_moved(self):
        return self._has_moved

    def set_has_moved(self, has_moved=True):
        self._has_moved = has_moved


class Rook(Piece):
    """Creates a Rook"""
    def __init__(self, color):
        super().__init__(color)

    # This is what will be called by the str('Piece Type') call
    def __str__(self):
        return 'WR' if self._color == 'WHITE' else 'BR'


class Knight(Piece):
    """Creates a Knight"""
    def __init__(self, color):
        super().__init__(color)

    # This is what will be called by the str('Piece Type') call
    def __str__(self):
        return 'WN' if self._color == 'WHITE' else 'BN'


class Bishop(Piece):
    """Creates a Bishop"""
    def __init__(self, color):
        super().__init__(color)

    # This is what will be called by the str('Piece Type') call
    def __str__(self):
        return 'WB' if self._color == 'WHITE' else 'BB'


class Queen(Piece):
    """Creates a Queen"""
    def __init__(self, color):
        super().__init__(color)

    # This is what will be called by the str('Piece Type') call
    def __str__(self):
        return 'WQ' if self._color == 'WHITE' else 'BQ'


class King(Piece):
    """Creates a King"""
    def __init__(self, color):
        super().__init__(color)

    # This is what will be called by the str('Piece Type') call
    def __str__(self):
        return 'WK' if self._color == 'WHITE' else 'BK'


# VERIFICATION METHODS
def verify_move(chess_piece, src_square, dest_square, board):
    """Verifies move of piece type"""

    # Column map used to pair string characters to integers
    COLUMN_MAP = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8
    }

    src_row = int(src_square[1])
    src_col = COLUMN_MAP[src_square[0].lower()]

    dest_row = int(dest_square[1])
    dest_col = COLUMN_MAP[dest_square[0].lower()]

    # PAWN VERIFICATION - Can move forward 1 or 2 squares at first turn and 1 square only after first turn
    if isinstance(chess_piece, Pawn):
        if chess_piece.get_color() == "WHITE":
            if dest_row == src_row + 1 and dest_col == src_col and is_path_clear(board, src_square, dest_square):
                return f"{dest_square[0]}{dest_row}" not in board

            elif (dest_row == src_row + 2 and dest_col == src_col and not chess_piece.has_moved()
                  and is_path_clear(board, src_square, dest_square)):
                return f"{dest_square[0]}{dest_row}" not in board and f"{src_square[0]}{src_row + 1}" not in board

            elif (dest_row == src_row + 1 and abs(dest_col - src_col) == 1
                  and is_path_clear(board, src_square, dest_square)):
                return f"{dest_square[0]}{dest_row}" in board
        else:
            if dest_row == src_row - 1 and dest_col == src_col and is_path_clear(board, src_square, dest_square):
                return f"{dest_square[0]}{dest_row}" not in board
            elif (dest_row == src_row - 2 and dest_col == src_col and not chess_piece.has_moved()
                  and is_path_clear(board, src_square, dest_square)):
                return f"{dest_square[0]}{dest_row}" not in board and f"{src_square[0]}{src_row - 1}" not in board

            elif (dest_row == src_row - 1 and abs(dest_col - src_col) == 1
                  and is_path_clear(board, src_square, dest_square)):
                return f"{dest_square[0]}{dest_row}" in board

        return False

    # ROOK VERIFICATION - Can move horizontally and vertically in unlimited squares
    elif isinstance(chess_piece, Rook):
        if (dest_row == src_row or dest_col == src_col) and is_path_clear(board, src_square, dest_square):
            return True
        return False

    # KNIGHT VERIFICATION - Can move in an L-pattern (3 row squares and 2 col squares)
    elif isinstance(chess_piece, Knight):
        row_diff = abs(dest_row - src_row)
        col_diff = abs(dest_col - src_col)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        return False

    # BISHOP VERIFICATION - Can move diagonally in unlimited squares
    elif isinstance(chess_piece, Bishop):
        if abs(dest_row - src_row) == abs(dest_col - src_col) and is_path_clear(board, src_square, dest_square):
            return True
        return False

    # QUEEN VERIFICATION - Can move unlimited squares in all directions
    elif isinstance(chess_piece, Queen):
        if (dest_row == src_row or dest_col == src_col or abs(dest_row - src_row) == abs(dest_col - src_col)) and is_path_clear(board, src_square, dest_square):
            return True
        return False

    # KING VERIFICATION - Can move 1 square in all directions
    elif isinstance(chess_piece, King):
        if abs(dest_row - src_row) <= 1 and abs(dest_col - src_col) <= 1:
            return True
        return False

    return False


def is_path_clear(board, src_square, dest_square):
    """Checks if path is clear meaning there is no piece from the same team blocking its move"""

    COLUMN_MAP = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8
    }

    src_col, src_row = src_square[0].lower(), int(src_square[1])
    dest_col, dest_row = dest_square[0].lower(), int(dest_square[1])

    src_col_num = COLUMN_MAP[src_col]
    dest_col_num = COLUMN_MAP[dest_col]

    if src_row == dest_row:  # Moving horizontally
        if src_col_num < dest_col_num:
            for col in range(src_col_num + 1, dest_col_num):
                if f"{list(COLUMN_MAP.keys())[col - 1]}{src_row}" in board:
                    return False
        else:
            for col in range(src_col_num - 1, dest_col_num, -1):
                if f"{list(COLUMN_MAP.keys())[col - 1]}{src_row}" in board:
                    return False
    elif src_col_num == dest_col_num:  # Moving vertically
        if src_row < dest_row:
            for row in range(src_row + 1, dest_row):
                if f"{src_col}{row}" in board:
                    return False
        else:
            for row in range(src_row - 1, dest_row, -1):
                if f"{src_col}{row}" in board:
                    return False
    else:  # Moving diagonally
        row_step = 1 if dest_row > src_row else -1
        col_step = 1 if dest_col_num > src_col_num else -1
        col, row = src_col_num + col_step, src_row + row_step
        while col != dest_col_num and row != dest_row:
            if f"{list(COLUMN_MAP.keys())[col - 1]}{row}" in board:
                return False
            col += col_step
            row += row_step
    return True


# EXCEPTION CLASSES
class ExecutionError(Exception):
    """Raises an execution error"""
    def __init__(self, message="This method or function cannot be executed."):
        self.message = message
        super().__init__(self.message)
