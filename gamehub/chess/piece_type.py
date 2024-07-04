from enum import Enum

class PieceType(Enum):
    KING = 'King'
    QUEEN = 'Queen'
    ROOK = 'Rook'
    BISHOP = 'Bishop'
    KNIGHT = 'Knight'
    PAWN = 'Pawn'

    @staticmethod
    def from_char(char):
        if char == 'K' or char == 'k':
            return PieceType.KING
        elif char == 'Q' or char == 'q':
            return PieceType.QUEEN
        elif char == 'R' or char == 'r':
            return PieceType.ROOK
        elif char == 'B' or char == 'b':
            return PieceType.BISHOP
        elif char == 'N' or char == 'n':
            return PieceType.KNIGHT
        elif char == 'P' or char == 'p':
            return PieceType.PAWN
        else:
            raise ValueError(f"Invalid character: {char}")