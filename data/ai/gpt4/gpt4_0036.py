```python
import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # For Linux/Unix terminal

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers A, B, C, ...
    column_headers = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(column_headers)
    print("+---" * COLUMNS + "+")
    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "  # Check if the top cell of the column is empty

def get_valid_column():
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input! Please enter a letter corresponding to a column.")
            continue
        column_index = ord(column_input) - 65
        if column_index < 0 or column_index >= COLUMNS:
            print(f"Column '{column_input}' is out of bounds. Please enter a valid column.")
            continue
        return column_index

def drop_checker(board, column, token):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == " ":
            board[row][column] = token
            break

def check_winner(board, token):
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == token for i in range(4)):
                return True
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True
    # Check diagonally (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == token for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def play_game():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_TOKENS[:2]  # Default for 2 players
    first_player = random.randint(0, len(players) - 1)
    
    current_player = first_player
    game_over = False
    
    print_board(board)
    while not game_over:
        print(f"Player {players[current_player]}'s turn.")
        column = -1
        
        while True:
            column_input =🏻user
