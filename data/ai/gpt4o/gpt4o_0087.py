import os
import random

# Constants for board and players
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

class Connect4:
    def __init__(self, rows=BOARD_ROWS, cols=BOARD_COLS, num_players=2):
        self.rows = rows
        self.cols = cols
        self.num_players = num_players
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.players = PLAYER_SYMBOLS[:num_players]
        self.current_player_index = random.randint(0, num_players - 1)
        self.current_player = self.players[self.current_player_index]

    def clear_screen(self):
        os.system('clear')

    def print_board(self):
        self.clear_screen()
        print("  " + "   ".join(chr(65 + i) for i in range(self.cols)))
        print("+" + "---+" * self.cols)
        for row in self.board:
            print("| " + " | ".join(row) + " |")
            print("+" + "---+" * self.cols)

    def check_input_validity(self, choice):
        if not choice.isalpha() or len(choice) != 1:
            return False
        col_index = ord(choice.upper()) - 65
        if col_index < 0 or col_index >= self.cols:
            return False
        if self.board[0][col_index] != ' ':
            return False
        return True

    def place_checker(self, choice):
        col_index = ord(choice.upper()) - 65
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col_index] == ' ':
                self.board[row][col_index] = self.current_player
                break

    def check_winner(self):
        # Horizontal check
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] == self.current_player and \
                   self.board[row][col + 1] == self.current_player and \
                   self.board[row][col + 2] == self.current_player and \
                   self.board[row][col + 3] == self.current_player:
                    return True

        # Vertical check
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col] == self.current_player and \
                   self.board[row + 2][col] == self.current_player and \
                   self.board[row + 3][col] == self.current_player:
                    return True

        # Diagonal check /
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col + 1] == self.current_player and \
                   self.board[row + 2][col + 2] == self.current_player and \
                   self.board[row + 3][col + 3] == self.current_player:
                    return True

        # Diagonal check \
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] == self.current_player and \
                   self.board[row - 1][col + 1] == self.current_player and \
                   self.board[row - 2][col + 2] == self.current_player and \
                   self.board[row - 3][col + 3] == self.current_player:
                    return True

        return False

    def check_draw(self):
        for row in range(self.rows):
            if ' ' in self.board[row]:
                return False
        return True

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        self.current_player = self.players[self.current_player_index]

    def play_game(self):
        self.print_board()
        while True:
            choice = input(f"Player {self.current_player}, please enter a column: ").strip()
            while not self.check_input_validity(choice):
                choice = input(f"Invalid input. Player {self.current_player}, please enter a valid column: ").strip()
            self.place_checker(choice)
            self.print_board()
            if self.check_winner():
                print(f"Player {self.current_player} won!")
                break
            elif self.check_draw():
                print("The game is a draw!")
                break
            self.switch_player()

if __name__ == "__main__":
    game = Connect4(num_players=2)
    game.play_game()
