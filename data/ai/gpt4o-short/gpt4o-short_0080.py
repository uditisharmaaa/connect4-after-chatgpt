import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Available players, up to 5

class ConnectFour:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = PLAYERS[:num_players]
        self.board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = random.choice(self.players)

    def print_board(self):
        os.system('clear')
        print("  A B C D E F G")
        for row in self.board:
            print("|" + "|".join(row) + "|")
        print("  " + "-" * 13)
        
    def is_valid_column(self, col):
        return 0 <= col < COLUMNS and self.board[0][col] == ' '

    def drop_piece(self, col):
        for row in reversed(self.board):
            if row[col] == ' ':
                row[col] = self.current_player
                break

    def change_player(self):
        current_index = self.players.index(self.current_player)
        self.current_player = self.players[(current_index + 1) % self.num_players]

    def is_winner(self):
        # Check horizontal, vertical, and diagonal (both directions) for win
        for c in range(COLUMNS - 3):
            for r in range(ROWS):
                if self.board[r][c] == self.current_player and all(self.board[r][c+i] == self.current_player for i in range(4)):
                    return True

        for c in range(COLUMNS):
            for r in range(ROWS - 3):
                if self.board[r][c] == self.current_player and all(self.board[r+i][c] == self.current_player for i in range(4)):
                    return True

        for c in range(COLUMNS - 3):
            for r in range(ROWS - 3):
                if self.board[r][c] == self.current_player and all(self.board[r+i][c+i] == self.current_player for i in range(4)):
                    return True

        for c in range(COLUMNS - 3):
            for r in range(3, ROWS):
                if self.board[r][c] == self.current_player and all(self.board[r-i][c+i] == self.current_player for i in range(4)):
                    return True

        return False

    def is_draw(self):
        return all(self.board[0][c] != ' ' for c in range(COLUMNS))

    def play(self):
        self.print_board()
        while True:
            try:
                col_letter = input(f"Player {self.current_player}, choose a column (A-G): ").upper()
                if col_letter < 'A' or col_letter > 'G':
                    raise ValueError("Input must be between A-G")
                
                column = ord(col_letter) - ord('A')
                if not self.is_valid_column(column):
                    raise ValueError("Column is full or invalid, choose another one.")
                
                self.drop_piece(column)
                self.print_board()
                
                if self.is_winner():
                    print(f"Player {self.current_player} wins!")
                    break

                if self.is_draw():
                    print("It's a draw!")
                    break

                self.change_player()
                
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    num_players = int(input("Enter number of players (2 to 5): "))
    if 2 <= num_players <= 5:
        game = ConnectFour(num_players)
        game.play()
    else:
        print("Invalid number of players. Please enter between 2 and 5.")
