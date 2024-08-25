# Author: Rafael Ayala
# GitHub username: rayala30
# Date: 5/25/24
# Description: Chessboard Variant (Atomic) Game


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
        if (dest_row == src_row or dest_col == src_col or abs(dest_row - src_row) == abs(
                dest_col - src_col)) and is_path_clear(board, src_square, dest_square):
            return True
        return False

    # KING VERIFICATION - Can move 1 square in all directions
    elif isinstance(chess_piece, King):
        if dest_square.lower() in board and isinstance(board[dest_square.lower()], Piece):
            return False
        return abs(dest_row - src_row) <= 1 and abs(dest_col - src_col) <= 1

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


# CHESS BOARD CLASS
class ChessBoard:
    """Creates a chessboard"""

    def __init__(self):
        self._board = {}
        self.reset_board()

    def get_board(self):
        """Gets board"""
        return self._board

    def reset_board(self):
        """Resets board to default state."""

        # Use dictionary to pair each board position with a default position for chess pieces
        # Use dictionary to dynamically update positions on the board
        # The dictionary does not contain empty spaces for memory efficiency
        self._board = {
            'a1': Rook('WHITE'), 'b1': Knight('WHITE'), 'c1': Bishop('WHITE'), 'd1': Queen('WHITE'),
            'e1': King('WHITE'), 'f1': Bishop('WHITE'), 'g1': Knight('WHITE'), 'h1': Rook('WHITE'),
            'a2': Pawn('WHITE'), 'b2': Pawn('WHITE'), 'c2': Pawn('WHITE'), 'd2': Pawn('WHITE'),
            'e2': Pawn('WHITE'), 'f2': Pawn('WHITE'), 'g2': Pawn('WHITE'), 'h2': Pawn('WHITE'),
            'a8': Rook('BLACK'), 'b8': Knight('BLACK'), 'c8': Bishop('BLACK'), 'd8': Queen('BLACK'),
            'e8': King('BLACK'), 'f8': Bishop('BLACK'), 'g8': Knight('BLACK'), 'h8': Rook('BLACK'),
            'a7': Pawn('BLACK'), 'b7': Pawn('BLACK'), 'c7': Pawn('BLACK'), 'd7': Pawn('BLACK'),
            'e7': Pawn('BLACK'), 'f7': Pawn('BLACK'), 'g7': Pawn('BLACK'), 'h7': Pawn('BLACK'),
        }

    def move_piece(self, src_pos, dest_pos, player_color):
        """Moves piece on a board"""

        src_pos_lower = src_pos.lower()
        dest_pos_lower = dest_pos.lower()

        if src_pos_lower not in self._board:
            # raise ValueError("Source position is not valid.")
            print("Source position is not valid.")
            return False

        piece = self._board.get(src_pos_lower)
        piece_move_verify = verify_move(piece, src_pos_lower, dest_pos_lower, self._board)

        if not piece:
            # raise ValueError("There is no piece at source position.")
            print("There is no piece at source position.")
            return False

        # Check if piece can move to location
        if not piece_move_verify:
            # raise ExecutionError("Piece cannot move to an invalid location. Path has to be clear for piece to move "
            #                      "(except for Knights) OR destined location is based on allowed movement"
            #                      " patterns for specific piece type according to traditional chess rules.")
            print("Piece cannot move to an invalid location. Path has to be clear for piece to move "
                  "(except for Knights) OR destined location is based on allowed movement"
                  " patterns for specific piece type according to traditional chess rules.")
            return False

        dest_piece = self._board.get(dest_pos_lower)
        if dest_piece:
            if dest_piece.get_color() == player_color:
                # raise ValueError("Cannot capture own piece.")
                print("Cannot capture own piece.")
                return False

            else:
                self.capture(src_pos_lower, dest_pos_lower, piece)
                return True

        else:
            # Update the destination position with capturing piece, if dest is empty
            self._board[dest_pos_lower] = piece
            # Remove piece from previous board source position
            del self._board[src_pos_lower]

        # SPECIAL PIECE CONDITIONS
        # Update pawn's moved status if it's a pawn
        if isinstance(piece, Pawn):
            piece.set_has_moved()

        return True

    def capture(self, src_pos, dest_pos, piece):
        """Source piece replaces destination piece"""
        del self._board[dest_pos.lower()]
        del self._board[src_pos.lower()]
        self._board[dest_pos.lower()] = piece

    def remove_piece(self, position):
        """Removes piece from a specified position"""
        if position in self._board:
            del self._board[position]
        else:
            pass

    def print_board(self):
        """Prints board to console"""

        # Top Border and Label
        pipe_sep = " | "
        print("       " + "     ".join("abcdefgh"))
        print("    " + "+" + "-----+" * 8)  # Prints 8 times for number of rows
        for row in range(8, 0, -1):
            # Prints row number first
            print(row, ' ', end=pipe_sep)  # Override default 'end' for print() method

            # Since columns are labeled letters, we need to use the ASCII values of the character labels
            for col in range(97, 105):
                column_pos = chr(col)  # col is converted to string character based on the ASCII ranges in the for loop

                # For example, c(col) + 8(row) is retrieved from the board dictionary as 'c8'
                # Get chess piece from dictionary board
                piece = self._board.get(f"{column_pos}{row}")

                # If there is a piece in the position it gets __str__ of Piece, else it is an empty space
                piece_str = str(piece) if piece else ' '
                print("{:^3}".format(piece_str), end=pipe_sep)
            print("  ", row)
            print("    " + "+" + "-----+" * 8)
        # Bottom Label
        print("       " + "     ".join("abcdefgh"))


# CHESS VAR CLASS
class ChessVar:
    """Create a chess variant game class"""

    def __init__(self):
        self._board = ChessBoard()
        self._player_white = "WHITE"
        self._player_black = "BLACK"
        self._player_turn = "WHITE"

    def print_board(self):
        self._board.print_board()

    def get_player_turn(self):
        """Gets player turn"""
        return self._player_turn

    def set_player_turn(self, player):
        """Sets player turn"""
        self._player_turn = player.upper()

    def get_game_state(self):
        """Gets game state. Returns winner or if game is unfinished"""
        white_king_present = False
        black_king_present = False

        for piece in self._board.get_board().values():
            # Check if King is still present for both players
            if isinstance(piece, King):
                if piece.get_color() == 'WHITE':
                    white_king_present = True
                elif piece.get_color() == 'BLACK':
                    black_king_present = True

        # If King is not present, determine winner
        if not white_king_present:
            return 'BLACK_WON'
        elif not black_king_present:
            return 'WHITE_WON'
        return 'UNFINISHED'

    def make_move(self, src_square, dest_square):
        """Makes move on board by specifying a source and destination position"""
        current_player = self._player_turn
        board = self._board
        piece = board.get_board().get(src_square.lower())

        # Check if there is a piece in source square
        if not piece:
            print("There is no piece at this source square.")
            return False

        # Check if it is current player's turn
        if piece.get_color() != current_player:
            print("It is not this player color's turn.")
            return False

        # Validate that the destination square is within the board's boundaries
        if len(dest_square) != 2 or dest_square[0] not in 'abcdefgh' or dest_square[1] not in '12345678':
            print("Invalid move. Destination square is outside the board's boundaries.")
            return False

        # Check if destination square is occupied
        dest_piece = board.get_board().get(dest_square.lower())

        if dest_piece:
            if piece.get_color() == dest_piece.get_color():
                print("Invalid move. Cannot move to a square occupied by a piece of the same color.")
                return False

            else:
                # If it is a valid move. Capture and explode
                board.capture(src_square.lower(), dest_square.lower(), piece)

                # After move completes, switch player
                if current_player == self._player_white:
                    self._player_turn = self._player_black
                else:
                    self._player_turn = self._player_white

                # Check if explosion captures a king
                king_captured = self.explode(dest_square.lower())
                if king_captured:
                    # Print and return winner
                    print(self.get_game_state())
                    return True

                return True

        else:
            # If square is empty, move the piece to the destination square
            move_successful = board.move_piece(src_square, dest_square, current_player.upper())

            # After move completes, switch player
            if current_player == self._player_white:
                self._player_turn = self._player_black
            else:
                self._player_turn = self._player_white

            if move_successful:
                return True

            if not move_successful:
                return False

    def explode(self, new_pos):
        """Removes pieces (8 squares) around the captor"""
        # Define column names
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Get the row and column of the exploded piece (detonator)
        exploded_row = int(new_pos[1])
        exploded_col = columns.index(new_pos[0])

        # Define the range of rows and columns to check for explosions
        row_range = range(max(1, exploded_row - 1), min(9, exploded_row + 2))
        col_range = range(max(0, exploded_col - 1), min(8, exploded_col + 2))

        # Initialize king_captured
        king_captured = False

        # Check if both kings are present before explosion
        white_king_present = any(
            isinstance(piece, King) and piece.get_color() == 'WHITE' for piece in self._board.get_board().values())
        black_king_present = any(
            isinstance(piece, King) and piece.get_color() == 'BLACK' for piece in self._board.get_board().values())

        # Proceed with explosion only if both kings are present
        if white_king_present and black_king_present:
            # Iterate over the surrounding positions
            for row in row_range:
                for col in col_range:
                    # Skip the exploded piece's position
                    if row == exploded_row and col == exploded_col:
                        continue

                    # Create the position string
                    exploded_pos = columns[col] + str(row)

                    # Check if there's a piece at the position to explode
                    piece = self._board.get_board().get(exploded_pos)

                    if piece:
                        # If the piece is not a pawn, remove it from the board
                        if not isinstance(piece, Pawn):
                            # Check if King is caught in explosion
                            if isinstance(piece, King):
                                king_captured = True
                            self._board.remove_piece(exploded_pos)

        # Remove the capturing piece itself after explosions are complete
        self._board.remove_piece(new_pos)

        return king_captured


# EXCEPTION CLASSES
class ExecutionError(Exception):
    """Raises an execution error"""

    def __init__(self, message="This method or function cannot be executed."):
        self.message = message
        super().__init__(self.message)


# MAIN CLASSES
def main():
    game1 = ChessVar()

    print("--------------------------------------------------------------------------------")
    game1.make_move('a2', 'a3')  # WHITE - PAWN MOVES
    game1.make_move('f7', 'f5')  # BLACK - PAWN MOVES
    game1.make_move('a3', 'a4')  # WHITE - PAWN MOVES
    game1.make_move('f5', 'f4')  # BLACK - PAWN MOVES

    game1.make_move('a1', 'a3')  # WHITE - ROOK MOVES
    game1.make_move('c7', 'c5')  # BLACK - PAWN MOVES
    game1.make_move('a3', 'h3')  # WHITE - ROOK MOVES
    game1.make_move('b8', 'c6')  # BLACK - KNIGHT MOVES

    game1.make_move('b1', 'a3')  # WHITE - KNIGHT MOVES
    game1.make_move('b7', 'b5')  # BLACK - PAWN MOVES
    game1.make_move('b2', 'b4')  # WHITE - PAWN MOVES
    game1.make_move('c8', 'b7')  # BLACK - BISHOP MOVES

    game1.make_move('f2', 'f3')  # WHITE - PAWN MOVES
    game1.make_move('d8', 'a5')  # BLACK - QUEEN MOVES
    game1.make_move('b4', 'c5')  # WHITE - PAWN MOVES & CAPTURES PAWN + EXPLODE
    game1.make_move('d7', 'd5')  # BLACK - PAWN MOVES

    game1.make_move('h3', 'h7')  # WHITE - ROOK MOVES & CAPTURES PAWN + EXPLODE
    game1.make_move('e8', 'd8')  # BLACK - KING MOVES
    game1.make_move('a4', 'b5')  # WHITE - PAWN MOVES & CAPTURES PAWN + EXPLODE
    game1.make_move('d8', 'c8')  # BLACK - KING MOVES

    game1.make_move('a3', 'b5')  # WHITE - KNIGHT MOVES
    game1.make_move('c8', 'b8')  # BLACK - KING MOVES
    game1.make_move('b5', 'a7')  # WHITE - KNIGHT MOVES & CAPTURES PAWN + EXPLODE = KING DEAD

    game1.print_board()

    game2 = ChessVar()
    # GAME 2
    game2.make_move('a2', 'a3')  # WHITE
    # print(game2.make_move('a1', 'a5'))
    game2.make_move('a7', 'a6')  # BLACK
    game2.make_move('h2', 'h4')  # WHITE
    game2.make_move('d7', 'd5')  # BLACK

    game2.make_move('h1', 'h3')  # WHITE
    game2.make_move('b8', 'c6')  # BLACK
    game2.make_move('a1', 'a2')  # WHITE
    game2.make_move('c8', 'h3')  # BLACK

    game2.make_move('g1', 'h3')  # WHITE

    game2.print_board()

    # game_readme_test = ChessVar()
    # print(game_readme_test.make_move('a2', 'a4'))  # output True
    # print(game_readme_test.make_move('g7', 'g5'))  # output True
    # game_readme_test.print_board()
    # print(game_readme_test.get_game_state())  # output UNFINISHED


if __name__ == '__main__':
    main()
