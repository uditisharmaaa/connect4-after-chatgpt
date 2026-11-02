import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Helper functions
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print Column Headers
    print("  " + "   ".join(chr(i + 65) for i in range(len(board[0]))))
    # Print Board Rows
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    if column.isalpha() and len(column) == 1:
        col_index = ord(column.upper()) - 65
        if 0 <= col_index < len(board[0]):
            return board[0][col_index] == " "
    return False

def get_valid_column(board):
    while True:
        column = input("Please enter a column: ").strip().upper()
        if is_valid_column(column, board):
            return ord(column) - 65
        else:
            print("Invalid input. Try again.")

def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            break

def is_winning_move(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == symbol for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def connect4():
    clear_screen()
    # Set up variables
    board = create_board(ROWS, COLS)
    num_players = MIN_PLAYERS  # You can adjust this for more players
    players = PLAYER_SYMBOLS[:num_players]
    turn = random.randint(0, num_players - 1)
    
    # Game loop
    while True:
        clear_screen()
        print_board(board)
        current_player = players[turn]
        print(f"Player {current_player}'s turn.")
        col = get_valid_column(board)
        place_checker(board, col, current_player)
        
        if is_winning_move(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch turn
        turn = (turn + 1) % num_players

# Run the game
if __name__ == "__main__":
    connect4()
