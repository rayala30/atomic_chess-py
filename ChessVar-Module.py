# Author: Rafael Ayala
# GitHub username: rayala30
# Date: 5/25/24
# Description: Chessboard Variant (Atomic) Game

from ChessBoard import *


class ChessVar:
    """Create a chess variant game class"""

    def __init__(self, board: ChessBoard):
        self._board = board
        self._player_white = "WHITE"
        self._player_black = "BLACK"
        self._player_turn = "WHITE"

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
            raise ExecutionError("There is no piece at this source square.")

        # Check if it is current player's turn
        if piece.get_color() != current_player:
            raise ExecutionError("It is not this player color's turn.")

        # Check if destination square is occupied
        dest_piece = board.get_board().get(dest_square.lower())

        if dest_piece:
            if piece.get_color() == dest_piece.get_color():
                raise ExecutionError("Invalid move. Cannot move to a square occupied by a piece of the same color.")
            else:
                # If it is a valid move. Capture and explode
                board.capture(src_square.lower(), dest_square.lower(), piece)

                # Check if explosion captures a king
                king_captured = self.explode(dest_square.lower())
                if king_captured:
                    # Print and return winner
                    print(self.get_game_state())
                    return self.get_game_state()
        else:
            # If square is empty, move the piece to the destination square
            board.move_piece(src_square, dest_square, current_player.upper())

        # After move completes, switch player
        if current_player == self._player_white:
            self._player_turn = self._player_black
        else:
            self._player_turn = self._player_white

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


# MAIN CLASSES
def main():
    chess_board = ChessBoard()
    game = ChessVar(chess_board)

    print()
    print("GAME START!")

    print("--------------------------------------------------------------------------------")
    game.make_move('a2', 'a3')  # WHITE
    game.make_move('f7', 'f5')  # BLACK
    game.make_move('a3', 'a4')  # WHITE
    game.make_move('f5', 'f4')  # BLACK

    game.make_move('a1', 'a3')  # WHITE
    game.make_move('c7', 'c5')  # BLACK
    game.make_move('a3', 'h3')  # WHITE
    game.make_move('b8', 'c6')  # BLACK

    game.make_move('b1', 'a3')  # WHITE
    game.make_move('b7', 'b5')  # BLACK
    game.make_move('b2', 'b4')  # WHITE
    game.make_move('c8', 'b7')  # BLACK

    game.make_move('f2', 'f3')  # WHITE
    game.make_move('d8', 'a5')  # BLACK
    game.make_move('b4', 'c5')  # WHITE (PAWN CAPTURE)
    game.make_move('d7', 'd5')  # BLACK

    game.make_move('h3', 'h7')  # WHITE (ROOK CAPTURE)
    game.make_move('e8', 'd8')  # BLACK
    game.make_move('a4', 'b5')  # WHITE (PAWN CAPTURE)
    game.make_move('d8', 'c8')  # BLACK
    #
    game.make_move('a3', 'b5')  # WHITE
    game.make_move('c8', 'b8')  # BLACK
    game.make_move('b5', 'a7')  # WHITE (PAWN CAPTURE, KING DEAD)

    chess_board.print_board()


if __name__ == '__main__':
    main()
