import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Functions
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    # Print rows of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_index(letter):
    return ord(letter.upper()) - 65

def valid_column(col, board):
    return 0 <= col < COLUMNS and board[0][col] == " "

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return

def check_horizontal(board, player):
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col+4] == [player] * 4:
                return True
    return False

def check_vertical(board, player):
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    return False

def check_diagonal(board, player):
    # Check descending diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check ascending diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def check_win(board, player):
    return (
        check_horizontal(board, player) or
        check_vertical(board, player) or
        check_diagonal(board, player)
    )

# Main logic
board = create_board()
print_board(board)

players = [CHECKERS[i] for i in range(PLAYERS)]
current_player = random.randint(0, PLAYERS - 1)

while True:
    print(f"Player {players[current_player]}, please enter a column:")
    col_input = input().strip()
    
    if len(col_input) != 1 or not col_input.isalpha():
        print("Invalid input. Please enter a valid column letter.")
        continue
    
    col = get_column_index(col_input)
    
    if not valid_column(col, board):
        print("Invalid column. Please try again.")
        continue
    
    drop_checker(board, col, players[current_player])
    print_board(board)
    
    if check_win(board, players[current_player]):
        print(f"Player {players[current_player]} won!")
        break
    
    if check_draw(board):
        print("It's a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
