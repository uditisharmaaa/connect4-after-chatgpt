import os
import random
import string
import sys

# ====== CONSTANTS ======
ROWS = 6           # Number of rows (default 6)
COLUMNS = 7        # Number of columns (default 7)
NUM_PLAYERS = 2    # Change this for more players (2-5)
WIN_COUNT = 4      # Number of same checker in a row to win (default 4)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ====== FUNCTIONS ======

def clear_screen():
    # Clear the terminal screen
    os.system('clear')  # For Linux/Unix

def create_board(rows, cols):
    # Initialize board with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column labels
    labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    print("+" + "---+" * len(labels))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(labels))

def input_column(player_checker, valid_cols):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_cols:
            print(f"Invalid input. Enter one of the columns: {', '.join(valid_cols)}")
        else:
            return valid_cols.index(user_input)

def find_row_to_place(board, col):
    # Finds the lowest empty row to place the checker in a column.
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            return row
    return None  # Column full

def place_checker(board, row, col, checker):
    board[row][col] = checker

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal (\) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    # Diagonal (/) check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def next_player(current, num_players):
    return (current + 1) % num_players

def main():
    # ----- SETUP -----
    # Apply constraints
    if COLUMNS > 26 or COLUMNS < 4 or ROWS < 4:
        print("Columns must be between 4 and 26 and rows >= 4.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)
    board = create_board(ROWS, COLUMNS)
    valid_cols = [string.ascii_uppercase[i] for i in range(COLUMNS)]
    player_symbols = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {player_symbols[current_player]} starts!\n")

    # ----- GAME LOOP -----
    game_over = False
    while not game_over:
        player_checker = player_symbols[current_player]
        col = input_column(player_checker, valid_cols)
        row = find_row_to_place(board, col)
        if row is None:
            print("Column is full. You lose your turn!")
            # Player loses turn. Move to next player.
        else:
            place_checker(board, row, col, player_checker)
            clear_screen()
            print_board(board)
            # Check if this player won:
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                game_over = True
                continue
            # Check for draw:
            if check_draw(board):
                print("It's a draw! No more moves possible.")
                game_over = True
                continue
        # Next player's turn
        current_player = next_player(current_player, NUM_PLAYERS)

if __name__ == '__main__':
    main()
