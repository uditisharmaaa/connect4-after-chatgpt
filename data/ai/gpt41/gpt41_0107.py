import os
import random
import sys

# ======================== CONSTANTS ========================
ROWS = 6           # Number of rows (can be changed for testing)
COLS = 7           # Number of columns (can be changed for testing, max 26)
NUM_PLAYERS = 2    # Set to 2 (can be 2-5 for wider testing)
CONNECT_N = 4      # Number to connect in a row to win

CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

# ======================== FUNCTIONS ========================

def clear_screen():
    # Works on Unix/Linux; you may change to 'cls' for Windows
    os.system('clear')

def create_board():
    # Creates a 2D list ROWS x COLS filled with spaces
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Display the column labels
    print("\n  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print()
    print("+" + "---+" * COLS)

    # Display the board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COLS)

def get_valid_column_input(board):
    valid = False
    while not valid:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print(f"Invalid input. Enter a single letter from A to {COLUMN_LABELS[-1]}.")
            continue
        col = ord(col_input) - ord("A")
        if board[0][col] != " ":
            print(f"Column {col_input} is full. You lose your turn.")
            return None  # Indicate invalid move and lost turn
        return col

def drop_checker(board, col, checker):
    # Start from bottom row, find first empty
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not be reached, unless column is full

def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - CONNECT_N + 1):
            if all(board[row][col+i] == checker for i in range(CONNECT_N)):
                return True
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - CONNECT_N + 1):
            if all(board[row+i][col] == checker for i in range(CONNECT_N)):
                return True
    # Diagonal (down-right) check
    for row in range(ROWS - CONNECT_N + 1):
        for col in range(COLS - CONNECT_N + 1):
            if all(board[row+i][col+i] == checker for i in range(CONNECT_N)):
                return True
    # Diagonal (down-left) check
    for row in range(ROWS - CONNECT_N + 1):
        for col in range(CONNECT_N - 1, COLS):
            if all(board[row+i][col-i] == checker for i in range(CONNECT_N)):
                return True
    return False

def check_draw(board):
    # If top row has any empty space, not a draw
    return all(cell != " " for cell in board[0])

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = choose_first_player(NUM_PLAYERS)

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player]} will go first!\n")

    while True:
        player_checker = players[current_player]
        print(f"Player {player_checker},", end=" ")
        col = get_valid_column_input(board)

        clear_screen()

        if col is not None:
            row, col_idx = drop_checker(board, col, player_checker)
            print_board(board)
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Lose turn if column is full (as per assignment requirements)
            print_board(board)
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nGame interrupted.")
