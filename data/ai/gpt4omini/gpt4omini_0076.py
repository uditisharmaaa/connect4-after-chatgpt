import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # Add more players if needed: ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A-G
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

def get_valid_input(current_player):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column >= chr(65 + COLUMNS):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        col_index = ord(column) - 65
        if is_column_full(col_index):
            print("Column is full. Please choose another column.")
            continue
        return col_index

def is_column_full(col):
    return all(board[row][col] != " " for row in range(ROWS))

def drop_piece(board, col, piece):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = piece
            return row

def check_win(board, piece):
    # Check horizontal, vertical, and diagonal wins
    return (check_horizontal(board, piece) or
            check_vertical(board, piece) or
            check_diagonal(board, piece))

def check_horizontal(board, piece):
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True
    return False

def check_vertical(board, piece):
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == piece for i in range(4)):
                return True
    return False

def check_diagonal(board, piece):
    # Check downward diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True
    # Check upward diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True
    return False

def check_draw():
    return all(board[row][col] != " " for row in range(ROWS) for col in range(COLUMNS))

# Game initialization
board = create_board()
current_player_index = random.randint(0, len(PLAYERS) - 1)

# Main game loop
while True:
    print_board(board)
    current_player = PLAYERS[current_player_index]
    col = get_valid_input(current_player)
    drop_piece(board, col, current_player)

    if check_win(board, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        break

    if check_draw():
        print_board(board)
        print("The game is a draw!")
        break

    current_player_index = (current_player_index + 1) % len(PLAYERS)
