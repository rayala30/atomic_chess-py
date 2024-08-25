# Author: Rafael Ayala
# GitHub username: rayala30
# Date: 5/25/24
# Description: Chessboard

from ChessPieces import *


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
            raise ValueError("Source position is not valid.")

        piece = self._board.get(src_pos_lower)
        piece_move_verify = verify_move(piece, src_pos_lower, dest_pos_lower, self._board)

        if not piece:
            raise ValueError("There is no piece at source position.")

        # Check if piece can move to location
        if not piece_move_verify:
            raise ExecutionError("Piece cannot move to an invalid location. Check if path is clear or allowed "
                                 "movement patterns for specific piece type according to traditional chess rules.")

        dest_piece = self._board.get(dest_pos_lower)
        if dest_piece:
            if dest_piece.get_color() == player_color:
                raise ValueError("Cannot capture own piece.")
            else:
                self.capture(src_pos_lower, dest_pos_lower, piece)

        else:
            # Update the destination position with capturing piece, if dest is empty
            self._board[dest_pos_lower] = piece
            # Remove piece from previous board source position
            del self._board[src_pos_lower]

        # SPECIAL PIECE CONDITIONS
        # Update pawn's moved status if it's a pawn
        if isinstance(piece, Pawn):
            piece.set_has_moved()

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
