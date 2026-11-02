import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Available checkers for up to 5 players

# Functions
def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    
    # Print column labels (A-G, etc.)
    column_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    
    # Print board with boundaries
    for row in board:
        print("+---" * len(board[0]) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    # Check valid letter and if column has space
    if column.isalpha() and len(column) == 1:
        idx = ord(column.upper()) - ord('A')
        return 0 <= idx < len(board[0]) and board[0][idx] == " "
    return False

def get_available_row(board, column_index):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return None

def place_checker(board, column, checker):
    col_idx = ord(column.upper()) - ord('A')
    row_idx = get_available_row(board, col_idx)
    if row_idx is not None:
        board[row_idx][col_idx] = checker

def check_winner(board, player_symbol):
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal win (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal win (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Game setup
def connect4():
    # Initialize game variables
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    random.shuffle(players)
    current_player_index = 0
    clear_screen()
    print_board(board)
    
    while True:
        # Current player's turn
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        # Input validation
        while True:
            choice = input().strip().upper()
            if is_valid_column(choice, board):
                break
            print("Invalid input. Please choose a valid column:")

        # Place checker & print board
        place_checker(board, choice, current_player)
        print_board(board)
        
        # Check if the game is won
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect4()
