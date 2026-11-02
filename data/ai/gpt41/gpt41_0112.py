import os
import random
import string
import sys

# ----- CONSTANTS -----
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # In order!
NUM_PLAYERS = 2  # CHANGE this to test different numbers of players (between 2 and 5)

WIN_LENGTH = 4  # Number of symbols in a row needed to win

# ----- BOARD CREATION -----
def create_board(rows, cols):
    """Returns a board initialized with spaces (' ')"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


# ----- PRINTING -----
def print_board(board):
    os.system('clear')  # If using Windows, change to 'cls'
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    # Print column letters
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)


# ----- INPUT VALIDATION -----
def input_valid_column(user_input, board):
    """Checks if user_input is a single cap letter and refers to a board column."""
    if (len(user_input) != 1 or
        user_input not in string.ascii_uppercase[:len(board[0])]):
        return False
    col_index = string.ascii_uppercase.index(user_input)
    # Check if the column is full
    if board[0][col_index] != ' ':
        return 'full'
    return True

def next_open_row(board, col):
    """Returns the row index of the lowest available row in the column."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None  # No row available

# ----- WIN CHECK -----
def is_winner(board, symbol):
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            # Only check from a cell containing the symbol.
            if board[r][c] != symbol:
                continue
            
            # Check right (horizontal)
            if c + WIN_LENGTH - 1 < cols and all(
                board[r][c+i] == symbol for i in range(WIN_LENGTH)):
                return True
            
            # Check down (vertical)
            if r + WIN_LENGTH - 1 < rows and all(
                board[r+i][c] == symbol for i in range(WIN_LENGTH)):
                return True
                
            # Check down-right (diagonal)
            if (r + WIN_LENGTH - 1 < rows and c + WIN_LENGTH - 1 < cols and
                all(board[r+i][c+i] == symbol for i in range(WIN_LENGTH))):
                return True
            # Check down-left (diagonal)
            if (r + WIN_LENGTH - 1 < rows and c - WIN_LENGTH + 1 >= 0 and
                all(board[r+i][c-i] == symbol for i in range(WIN_LENGTH))):
                return True
    return False

# ----- DRAW CHECK -----
def is_draw(board):
    # If top row is full, the board is full (since pieces drop from top)
    return all(cell != ' ' for cell in board[0])

# ----- MAIN GAME FUNCTION -----
def connect4():
    # Check number of players validity
    num_players = NUM_PLAYERS
    if num_players < MIN_PLAYERS or num_players > MAX_PLAYERS:
        print(f"NUM_PLAYERS must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        sys.exit(1)
    players = PLAYER_SYMBOLS[:num_players]

    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select starting player
    curr_player_idx = random.randint(0, num_players-1)
    
    print_board(board)
    print(f"Player {players[curr_player_idx]} goes first!")

    while True:
        print()
        player_symbol = players[curr_player_idx]
        user_input = ''
        while True:
            user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
            validation = input_valid_column(user_input, board)
            if validation == True:
                break
            elif validation == 'full':
                print("Column is full. Turn lost!")
                curr_player_idx = (curr_player_idx + 1) % num_players
                break  # Lose turn, don't repeat input
            else:
                print("Invalid input. Please choose a valid, non-full column (A-G).")
        
        if validation != 'full':
            col = string.ascii_uppercase.index(user_input)
            row = next_open_row(board, col)
            if row is not None:
                board[row][col] = player_symbol
            print_board(board)

            # Check for win
            if is_winner(board, player_symbol):
                print(f"Player {player_symbol} won!")
                break

            # Check for draw
            if is_draw(board):
                print("Draw! The board is full and nobody has four in a row.")
                break

        # Next player's turn
        curr_player_idx = (curr_player_idx + 1) % num_players

if __name__ == "__main__":
    connect4()
