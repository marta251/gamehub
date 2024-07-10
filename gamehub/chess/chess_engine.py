import subprocess

class ChessEngine:
    def __init__(self):
        self.process = subprocess.Popen(['stockfish'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.initialize_engine()
    
    def initialize_engine(self) -> None:
        init_commands = [
            'uci\n',
            'setoption name Hash value 128\n',
            'isready\n'
        ]
        for command in init_commands:
            self.process.stdin.write(command)
            self.process.stdin.flush()
        # Wait for 'readyok'
        while True:
            if 'readyok' in self.process.stdout.readline():
                break
    
    def get_move(self, fen : str) -> tuple[int, int, int, int]:
        commands = [
            f'position fen {fen}\n',
            'go depth 20\n'
        ]
        for command in commands:
            self.process.stdin.write(command)
            self.process.stdin.flush()
        
        best_move = None
        while True:
            output = self.process.stdout.readline().strip()
            if 'bestmove' in output:
                best_move = output.split()[1]
                break
        return self.convert_algebraic_to_coordinates(best_move)
    
    def convert_algebraic_to_coordinates(self, algebraic: str) -> tuple[int, int, int, int]:
        return ord(algebraic[0]) - 97, 8 - int(algebraic[1]), ord(algebraic[2]) - 97, 8 - int(algebraic[3])
    
    def close(self) -> None:
        self.process.stdin.write('quit\n')
        self.process.stdin.flush()
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()
        self.process.wait()