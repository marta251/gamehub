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
        #diagonal
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


piece = ChessPiece(PieceType.BISHOP, 'w', (0, 3))
print (cb.ChessBoard("8/8/8/B3K3/8/8/8/8 w KQkq - 0 1").matrix)
print(piece.legal_moves(cb.ChessBoard("8/8/8/B3k3/8/8/8/8 w KQkq - 0 1").matrix))
print(piece.legal_moves(cb.ChessBoard("8/8/8/B3K3/8/8/8/8 w KQkq - 0 1").matrix)         )


