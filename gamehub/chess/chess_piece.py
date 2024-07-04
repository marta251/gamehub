from gamehub.chess.piece_type import PieceType
import gamehub.chess.chess_board as cb

class ChessPiece:

    def __init__(self, piece: PieceType, color: str, position: tuple[int, int]) -> None:
        self.piece = piece
        self.color = color
        self.position = position

    def opposite_color_pieces(self) -> str:
        if self.color == 'b':
            return ['P', 'R', 'N', 'B', 'Q', 'K']
        else:
            return ['p', 'r', 'n', 'b', 'q', 'k']


    def legal_moves(self, matrix : list[list[str]]) -> list[tuple[int, int]]:
        #if is not pinned and not under check
        if self.piece == PieceType.PAWN:
            return self.pawn_moves(matrix)
        elif self.piece == PieceType.KNIGHT:
            return self.knight_moves(matrix)
        elif self.piece == PieceType.BISHOP:
            return self.bishop_moves(matrix)
        elif self.piece == PieceType.ROOK:
            return self.rook_moves(matrix)
        elif self.piece == PieceType.QUEEN:
            return self.queen_moves(matrix)
        elif self.piece == PieceType.KING:
            return self.king_moves(matrix)
        else:
            raise ValueError("Invalid piece type")

    def rook_moves(self, matrix : list[list[str]]) -> list[tuple[int, int]]:
        moves = []
        #horizontal
        x = self.position[0]
        #while there is an empty space you can move there
        while x + 1 < 8 and matrix[self.position[1]][x + 1] == " ":
            x += 1
            moves.append((x, self.position[1]))
            #if there is a piece of the opposite color you can take it (and stop)
            if x + 1 < 8 and matrix[self.position[1]][x+1] != " " and matrix[self.position[1]][x+1] in self.opposite_color_pieces():
                moves.append((x+1, self.position[1]))
                break
        x = self.position[0]
        while x - 1 >= 0 and matrix[self.position[1]][x - 1] == " ":
            x -= 1
            moves.append((x, self.position[1]))
            if x - 1 >= 0 and matrix[self.position[1]][x-1] != " " and matrix[self.position[1]][x-1] in self.opposite_color_pieces():
                moves.append((x-1, self.position[1]))
                break
        #vertical
        y = self.position[1]
        while y + 1 < 8 and matrix[y + 1][self.position[0]] == " ":
            y += 1
            moves.append((self.position[0], y))
            if y + 1 < 8 and matrix[y+1][self.position[0]] != " " and matrix[y+1][self.position[0]] in self.opposite_color_pieces():
                moves.append((self.position[0], y+1))
                break
        y = self.position[1]
        while y - 1 >= 0 and matrix[y - 1][self.position[0]] == " ":
            y -= 1
            moves.append((self.position[0], y))
            if y-1 >= 0 and matrix[y-1][self.position[0]] != " " and matrix[y-1][self.position[0]] in self.opposite_color_pieces():
                moves.append((self.position[0], y-1))
                break
        return moves

    def bishop_moves(self, matrix : list[list[str]]) -> list[tuple[int, int]]:
        moves = []
        #first diagonal
        x = self.position[0]
        y = self.position[1]
        #while there is an empty space you can move there
        while x + 1 < 8 and y + 1 < 8 and matrix[y + 1][x + 1] == " ":
            x += 1
            y += 1
            moves.append((x, y))
            #if there is a piece of the opposite color you can take it (and stop)
            if x + 1 < 8 and y + 1 < 8 and matrix[y+1][x+1] != " " and matrix[y+1][x+1] in self.opposite_color_pieces():
                moves.append((x+1, y+1))
                break
        x = self.position[0]
        y = self.position[1]
        while x - 1 >= 0 and y - 1 >= 0 and matrix[y - 1][x - 1] == " ":
            x -= 1
            y -= 1
            moves.append((x, y))
            if x - 1 >= 0 and y - 1 >= 0 and matrix[y-1][x-1] != " " and matrix[y-1][x-1] in self.opposite_color_pieces():
                moves.append((x-1, y-1))
                break
        #second diagonal
        x = self.position[0]
        y = self.position[1]
        while x + 1 < 8 and y - 1 >= 0 and matrix[y - 1][x + 1] == " ":
            x += 1
            y -= 1
            moves.append((x, y))
            if x + 1 < 8 and y - 1 >= 0 and matrix[y-1][x+1] != " " and matrix[y-1][x+1] in self.opposite_color_pieces():
                moves.append((x+1, y-1))
                break
        x = self.position[0]
        y = self.position[1]
        while x - 1 >= 0 and y + 1 < 8 and matrix[y + 1][x - 1] == " ":
            x -= 1
            y += 1
            moves.append((x, y))
            if x - 1 >= 0 and y + 1 < 8 and matrix[y+1][x-1] != " " and matrix[y+1][x-1] in self.opposite_color_pieces():
                moves.append((x-1, y+1))
                break
        return moves
    
    def knight_moves(self, matrix : list[list[str]]) -> list[tuple[int, int]]:
        moves = []
        x = self.position[0]
        y = self.position[1]
        if x + 2 < 8 and y + 1 < 8 and (matrix[y+1][x+2] == " " or matrix[y+1][x+2] in self.opposite_color_pieces()):
            moves.append((x+2, y+1))
        if x + 2 < 8 and y - 1 >= 0 and (matrix[y-1][x+2] == " " or matrix[y-1][x+2] in self.opposite_color_pieces()):
            moves.append((x+2, y-1))
        if x - 2 >= 0 and y + 1 < 8 and (matrix[y+1][x-2] == " " or matrix[y+1][x-2] in self.opposite_color_pieces()):
            moves.append((x-2, y+1))
        if x - 2 >= 0 and y - 1 >= 0 and (matrix[y-1][x-2] == " " or matrix[y-1][x-2] in self.opposite_color_pieces()):
            moves.append((x-2, y-1))
        if x + 1 < 8 and y + 2 < 8 and (matrix[y+2][x+1] == " " or matrix[y+2][x+1] in self.opposite_color_pieces()):
            moves.append((x+1, y+2))
        if x + 1 < 8 and y - 2 >= 0 and (matrix[y-2][x+1] == " " or matrix[y-2][x+1] in self.opposite_color_pieces()):
            moves.append((x+1, y-2))
        if x - 1 >= 0 and y + 2 < 8 and (matrix[y+2][x-1] == " " or matrix[y+2][x-1] in self.opposite_color_pieces()):
            moves.append((x-1, y+2))
        if x - 1 >= 0 and y - 2 >= 0 and (matrix[y-2][x-1] == " " or matrix[y-2][x-1] in self.opposite_color_pieces()):
            moves.append((x-1, y-2))
        return moves
    
    def queen_moves(self, matrix : list[list[str]]) -> list[tuple[int, int]]:
        return self.rook_moves(matrix) + self.bishop_moves(matrix)
    
    def pawn_moves(self, matrix : list[list[str]]) -> list[tuple[int, int]]:
        moves = []
        x = self.position[0]
        y = self.position[1]
        if self.color == 'b':
            # first move
            if y == 1 and matrix[y+1][x] == " " and matrix[y+2][x] == " ":
                moves.append((x, y+2))
            if y == 1 and matrix[y+1][x] == " ": 
                moves.append((x, y+1))
            if y > 1 and y + 1 < 8 and matrix[y+1][x] == " ":
                moves.append((x, y+1))
            # diagonal captures
            if x + 1 < 8 and y + 1 < 8 and matrix[y+1][x+1] in self.opposite_color_pieces():
                moves.append((x+1, y+1))
            if x - 1 >= 0 and y + 1 < 8 and matrix[y+1][x-1] in self.opposite_color_pieces():
                moves.append((x-1, y+1))
        else:
            # first move
            if y == 6 and matrix[y-1][x] == " " and matrix[y-2][x] == " ":
                moves.append((x, y-2))
            if y == 6 and matrix[y-1][x] == " ":
                moves.append((x, y-1))
            if y < 6 and y - 1 >= 0 and matrix[y-1][x] == " ":
                moves.append((x, y-1))
            # diagonal captures
            if x + 1 < 8 and y - 1 >= 0 and matrix[y-1][x+1] in self.opposite_color_pieces():
                moves.append((x+1, y-1))
            if x - 1 >= 0 and y - 1 >= 0 and matrix[y-1][x-1] in self.opposite_color_pieces():
                moves.append((x-1, y-1))
        return moves
    
    # check if the king of my color is under attack
    def king_under_attack(self, matrix : list[list[str]]) -> bool:
        if self.color == 'b':
            opposite_color = 'w'
        else:
            opposite_color = 'b'
        for i in range(8):
            for j in range(8):
                if matrix[i][j] == 'K' and opposite_color == 'b':
                    king_position = (j, i)
                if matrix[i][j] == 'k' and opposite_color == 'w':
                    king_position = (j, i)
        for i in range(8):
            for j in range(8):
                if matrix[i][j] in self.opposite_color_pieces() and matrix[i][j] != 'K' and matrix[i][j] != 'k':
                    piece = ChessPiece(PieceType.from_char(matrix[i][j]), opposite_color, (j, i))
                    if king_position in piece.legal_moves(matrix):
                        return True
        return False
    