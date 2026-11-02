import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKER_SIGNS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def init_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear screen
    col_labels = ' '.join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(row) + '+')

# Place a checker on the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    return check_horizontal(board, checker) or check_vertical(board, checker) or check_diagonal(board, checker)

def check_horizontal(board, checker):
    for row in board:
        for col in range(len(row) - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    return False

def check_vertical(board, checker):
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    return False

def check_diagonal(board, checker):
    # Check left-to-right diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check right-to-left diagonals
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for a draw (no empty spaces)
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Convert column letter to index
def column_to_index(column):
    return ord(column.upper()) - ord('A')

# Main game function
def connect_four():
    board = init_board(ROWS, COLUMNS)
    num_players = 2  # Set to 2 for this assignment
    checkers = CHECKER_SIGNS[:num_players]
    current_player = random.choice(range(num_players))

    print_board(board)

    while True:
        player_checker = checkers[current_player]
        print(f"Player {player_checker}, please enter a column:")

        while True:
            try:
                column = input().strip().upper()
                if len(column) != 1 or not column.isalpha():
                    raise ValueError
                col_index = column_to_index(column)
                if col_index < 0 or col_index >= COLUMNS:
                    raise ValueError
                if place_checker(board, col_index, player_checker):
                    break
                else:
                    print("Column is full! Try another column.")
            except ValueError:
                print("Invalid input! Enter a valid column letter.")

        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    connect_four()
