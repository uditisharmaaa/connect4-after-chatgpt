import os
import random

# Constants for the board size and number of players
MAX_COLUMNS = 26
DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to initialize the game board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the game board
def print_board(board):
    os.system('clear')
    cols = len(board[0])
    print("  " + "   ".join([chr(65 + i) for i in range(cols)]))
    print("+---" * cols + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * cols + "+")

# Function to check for a win condition
def check_win(board, checkers):
    rows, cols = len(board), len(board[0])
    for c in checkers:
        # Check horizontal
        for row in board:
            if any(row[i:i+4] == [c] * 4 for i in range(cols - 3)):
                return True
        # Check vertical
        for col in range(cols):
            if any(board[i][col] == c and board[i+1][col] == c and 
                   board[i+2][col] == c and board[i+3][col] == c 
                   for i in range(rows - 3)):
                return True
        # Check diagonal (down-right)
        for i in range(rows - 3):
            for j in range(cols - 3):
                if all(board[i+k][j+k] == c for k in range(4)):
                    return True
        # Check diagonal (up-right)
        for i in range(3, rows):
            for j in range(cols - 3):
                if all(board[i-k][j+k] == c for k in range(4)):
                    return True
    return False

# Function to check for a draw condition
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Function to handle a player's turn
def player_turn(board, player_checker):
    cols = len(board[0])
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if column_input in [chr(65 + i) for i in range(cols)]:
            col_index = ord(column_input) - 65
            for row in reversed(board):
                if row[col_index] == " ":
                    row[col_index] = player_checker
                    return
            print("Column is full! Turn is lost.")
            return
        else:
            print("Invalid input! Please try again.")

# Main game function
def play_game():
    board = create_board(DEFAULT_ROWS, DEFAULT_COLUMNS)
    players = CHECKERS[:DEFAULT_PLAYERS]
    random.shuffle(players)
    current_player = 0
    
    while True:
        print_board(board)
        player_turn(board, players[current_player])
        if check_win(board, players):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % DEFAULT_PLAYERS

play_game()
