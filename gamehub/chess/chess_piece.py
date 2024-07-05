class ChessPiece:

    #TODO: arroccamento, en passant, promozione

    def __init__(self, piece_char: str, position: tuple[int, int]) -> None:
        # if the piece is uppercase it is white, otherwise it is black
        self.piece_char = piece_char
        
        if piece_char.isupper():
            self.color = 'w'
        else:
            self.color = 'b'
        
        # set the piece type
        if piece_char == 'P' or piece_char == 'p':
            self.piece = 'Pawn'
        elif piece_char == 'R' or piece_char == 'r':
            self.piece = 'Rook'
        elif piece_char == 'N' or piece_char == 'n':
            self.piece = 'Knight'
        elif piece_char == 'B' or piece_char == 'b':
            self.piece = 'Bishop'
        elif piece_char == 'Q' or piece_char == 'q':
            self.piece = 'Queen'
        elif piece_char == 'K' or piece_char == 'k':
            self.piece = 'King'
        else:
            raise ValueError("Invalid piece")


        self.position = position

    def __repr__(self) -> str:
        return f"ChessPiece(piece={self.piece}, color='{self.color}', position={self.position})"
    

    def is_enemy(self, piece: 'ChessPiece') -> bool:
        return self.color != piece.color
    

    def opposite_color_pieces(self) -> list['ChessPiece']:
        if self.color == 'b':
            return ['P', 'R', 'N', 'B', 'Q', 'K']
        else:
            return ['p', 'r', 'n', 'b', 'q', 'k']


    def legal_moves(self, matrix : list[list['ChessPiece']], check_king_under_attack=True) -> list[tuple[int, int]]:
        #if is not pinned and not under check
        if self.piece == 'Pawn':
            moves =  self.pawn_moves(matrix)
        elif self.piece == 'Knight':
            moves = self.knight_moves(matrix)
        elif self.piece == 'Bishop':
            moves = self.bishop_moves(matrix)
        elif self.piece == 'Rook':
            return self.rook_moves(matrix)
        elif self.piece == 'Queen':
            moves = self.queen_moves(matrix)
        elif self.piece == 'King':
            moves = self.king_moves(matrix)
        else:
            raise ValueError("Invalid piece type")
        
        #remove moves that put the king under attack
        if check_king_under_attack:
            for move in moves:
                new_matrix = [row.copy() for row in matrix]
                piece = matrix[self.position[1]][self.position[0]]
                new_matrix[self.position[1]][self.position[0]] = None
                new_matrix[move[1]][move[0]] = piece
                if self.king_under_attack(new_matrix):
                    moves.remove(move)
        
        return moves
            

    def rook_moves(self, matrix : list[list['ChessPiece']]) -> list[tuple[int, int]]:
        moves = []
        #horizontal
        x = self.position[0]
        #while there is an empty space you can move there
        while x + 1 < 8 and matrix[self.position[1]][x + 1] == None:
            x += 1
            moves.append((x, self.position[1]))
            #if there is a piece of the opposite color you can take it (and stop)
            if x + 1 < 8 and matrix[self.position[1]][x+1] != None and matrix[self.position[1]][x+1].is_enemy(self):
                moves.append((x+1, self.position[1]))
                break
        x = self.position[0]
        while x - 1 >= 0 and matrix[self.position[1]][x - 1] == None:
            x -= 1
            moves.append((x, self.position[1]))
            if x - 1 >= 0 and matrix[self.position[1]][x-1] != None and matrix[self.position[1]][x-1].is_enemy(self):
                moves.append((x-1, self.position[1]))
                break
        #vertical
        y = self.position[1]
        while y + 1 < 8 and matrix[y + 1][self.position[0]] == None:
            y += 1
            moves.append((self.position[0], y))
            if y + 1 < 8 and matrix[y+1][self.position[0]] != None and matrix[y+1][self.position[0]].is_enemy(self):
                moves.append((self.position[0], y+1))
                break
        y = self.position[1]
        while y - 1 >= 0 and matrix[y - 1][self.position[0]] == None:
            y -= 1
            moves.append((self.position[0], y))
            if y-1 >= 0 and matrix[y-1][self.position[0]] != None and matrix[y-1][self.position[0]].is_enemy(self):
                moves.append((self.position[0], y-1))
                break
        return moves

    def bishop_moves(self, matrix : list[list['ChessPiece']]) -> list[tuple[int, int]]:
        moves = []
        #first diagonal
        x = self.position[0]
        y = self.position[1]
        #while there is an empty space you can move there
        while x + 1 < 8 and y + 1 < 8 and matrix[y + 1][x + 1] == None:
            x += 1
            y += 1
            moves.append((x, y))
            #if there is a piece of the opposite color you can take it (and stop)
            if x + 1 < 8 and y + 1 < 8 and matrix[y+1][x+1] != None and matrix[y+1][x+1].is_enemy(self):
                moves.append((x+1, y+1))
                break
        x = self.position[0]
        y = self.position[1]
        while x - 1 >= 0 and y - 1 >= 0 and matrix[y - 1][x - 1] == None:
            x -= 1
            y -= 1
            moves.append((x, y))
            if x - 1 >= 0 and y - 1 >= 0 and matrix[y-1][x-1] != None and matrix[y-1][x-1].is_enemy(self):
                moves.append((x-1, y-1))
                break
        #second diagonal
        x = self.position[0]
        y = self.position[1]
        while x + 1 < 8 and y - 1 >= 0 and matrix[y - 1][x + 1] == None:
            x += 1
            y -= 1
            moves.append((x, y))
            if x + 1 < 8 and y - 1 >= 0 and matrix[y-1][x+1] != None and matrix[y-1][x+1].is_enemy(self):
                moves.append((x+1, y-1))
                break
        x = self.position[0]
        y = self.position[1]
        while x - 1 >= 0 and y + 1 < 8 and matrix[y + 1][x - 1] == None:
            x -= 1
            y += 1
            moves.append((x, y))
            if x - 1 >= 0 and y + 1 < 8 and matrix[y+1][x-1] != None and matrix[y+1][x-1].is_enemy(self):
                moves.append((x-1, y+1))
                break
        return moves
    
    def knight_moves(self, matrix : list[list['ChessPiece']]) -> list[tuple[int, int]]:
        moves = []
        x = self.position[0]
        y = self.position[1]
        if x + 2 < 8 and y + 1 < 8 and (matrix[y+1][x+2] == None or (matrix[y+1][x+2] != None and matrix[y+1][x+2].is_enemy(self))):
            moves.append((x+2, y+1))
        if x + 2 < 8 and y - 1 >= 0 and (matrix[y-1][x+2] == None or (matrix[y-1][x+2] != None and matrix[y-1][x+2].is_enemy(self))):
            moves.append((x+2, y-1))
        if x - 2 >= 0 and y + 1 < 8 and (matrix[y+1][x-2] == None or (matrix[y+1][x-2] != None and matrix[y+1][x-2].is_enemy(self))):
            moves.append((x-2, y+1))
        if x - 2 >= 0 and y - 1 >= 0 and (matrix[y-1][x-2] == None or (matrix[y-1][x-2] != None and matrix[y-1][x-2].is_enemy(self))):
            moves.append((x-2, y-1))
        if x + 1 < 8 and y + 2 < 8 and (matrix[y+2][x+1] == None or (matrix[y+2][x+1] != None and matrix[y+2][x+1].is_enemy(self))):
            moves.append((x+1, y+2))
        if x + 1 < 8 and y - 2 >= 0 and (matrix[y-2][x+1] == None or (matrix[y-2][x+1] != None and matrix[y-2][x+1].is_enemy(self))):
            moves.append((x+1, y-2))
        if x - 1 >= 0 and y + 2 < 8 and (matrix[y+2][x-1] == None or (matrix[y+2][x-1] != None and matrix[y+2][x-1].is_enemy(self))):
            moves.append((x-1, y+2))
        if x - 1 >= 0 and y - 2 >= 0 and (matrix[y-2][x-1] == None or (matrix[y-2][x-1] != None and matrix[y-2][x-1].is_enemy(self))):
            moves.append((x-1, y-2))
        return moves
    
    def queen_moves(self, matrix : list[list['ChessPiece']]) -> list[tuple[int, int]]:
        return self.rook_moves(matrix) + self.bishop_moves(matrix)
    
    def pawn_moves(self, matrix : list[list['ChessPiece']]) -> list[tuple[int, int]]:
        moves = []
        x = self.position[0]
        y = self.position[1]
        if self.color == 'b':
            # first move
            if y == 1 and matrix[y+1][x] == None and matrix[y+2][x] == None:
                moves.append((x, y+2))
            if y == 1 and matrix[y+1][x] == None: 
                moves.append((x, y+1))
            if y > 1 and y + 1 < 8 and matrix[y+1][x] == None:
                moves.append((x, y+1))
            # diagonal captures
            if x + 1 < 8 and y + 1 < 8 and matrix[y+1][x+1] != None and matrix[y+1][x+1].is_enemy(self):
                moves.append((x+1, y+1))
            if x - 1 >= 0 and y + 1 < 8 and matrix[y+1][x-1] != None and matrix[y+1][x-1].is_enemy(self):
                moves.append((x-1, y+1))
        else:
            # first move
            if y == 6 and matrix[y-1][x] == None and matrix[y-2][x] == None:
                moves.append((x, y-2))
            if y == 6 and matrix[y-1][x] == None:
                moves.append((x, y-1))
            if y < 6 and y - 1 >= 0 and matrix[y-1][x] == None:
                moves.append((x, y-1))
            # diagonal captures
            if x + 1 < 8 and y - 1 >= 0 and matrix[y-1][x+1] != None and matrix[y-1][x+1].is_enemy(self):
                moves.append((x+1, y-1))
            if x - 1 >= 0 and y - 1 >= 0 and matrix[y-1][x-1] != None and matrix[y-1][x-1].is_enemy(self):
                moves.append((x-1, y-1))
        return moves
    
    
    def king_moves(self, matrix : list[list['ChessPiece']]) -> list[tuple[int, int]]:
        moves = []
        x = self.position[0]
        y = self.position[1]
        if x + 1 < 8 and (matrix[y][x+1] == None or matrix[y][x+1].is_enemy(self)):
            moves.append((x+1, y))
        if x - 1 >= 0 and (matrix[y][x-1] == None or matrix[y][x-1].is_enemy(self)):
            moves.append((x-1, y))
        if y + 1 < 8 and (matrix[y+1][x] == None or matrix[y+1][x].is_enemy(self)):
            moves.append((x, y+1))
        if y - 1 >= 0 and (matrix[y-1][x] == None or matrix[y-1][x].is_enemy(self)):
            moves.append((x, y-1))
        if x + 1 < 8 and y + 1 < 8 and (matrix[y+1][x+1] == None or matrix[y+1][x+1].is_enemy(self)):
            moves.append((x+1, y+1))
        if x + 1 < 8 and y - 1 >= 0 and (matrix[y-1][x+1] == None or matrix[y-1][x+1].is_enemy(self)):
            moves.append((x+1, y-1))
        if x - 1 >= 0 and y + 1 < 8 and (matrix[y+1][x-1] == None or matrix[y+1][x-1].is_enemy(self)):
            moves.append((x-1, y+1))
        if x - 1 >= 0 and y - 1 >= 0 and (matrix[y-1][x-1] == None or matrix[y-1][x-1].is_enemy(self)):
            moves.append((x-1, y-1))
        return moves
    
    
    # check if the king of my color is under attack
    def king_under_attack(self, matrix : list[list['ChessPiece']]) -> bool:
        if self.color == 'b':
            opposite_color = 'w'
        else:
            opposite_color = 'b'
        for i in range(8):
            for j in range(8):
                if matrix[i][j]!=None and matrix[i][j].piece_char == 'K' and self.color == 'w':
                    king_position = (j, i)
                if matrix[i][j]!=None and matrix[i][j].piece_char == 'k' and self.color == 'b':
                    king_position = (j, i)
        for i in range(8):
            for j in range(8):
                if matrix[i][j] != None and matrix[i][j].is_enemy(self) and matrix[i][j].piece_char != 'K' and matrix[i][j].piece_char != 'k':
                    piece_moves = matrix[i][j].legal_moves(matrix, False)
                    if king_position in piece_moves:
                        return True
        return False