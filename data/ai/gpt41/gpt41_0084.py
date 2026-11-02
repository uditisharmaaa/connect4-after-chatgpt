import os
import random
import string

# ----- Constants ----- #
ROWS = 6
COLS = 7
NUM_PLAYERS = 2   # Change this value (2-5) for more players
WIN_LENGTH = 4    # Number of connected checkers needed to win

CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# ----- Helper Functions ----- #

def clear_screen():
    # Clear the terminal screen
    os.system('clear')  # For Unix/Linux
    # For Windows, use 'cls'

def create_board():
    # Initialize the game board as a list of lists
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print the column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_column_index(col_label):
    # Convert column letter to index
    if col_label in COLUMN_LABELS:
        return COLUMN_LABELS.index(col_label)
    return -1

def is_valid_column_choice(col_input):
    # Check if the input is a valid column label
    return col_input in COLUMN_LABELS

def is_column_full(board, col_idx):
    # If the top cell in the column is not empty, the column is full
    return board[0][col_idx] != " "

def get_next_open_row(board, col_idx):
    # Return the bottom-most open row in a column
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            return row_idx
    return None  # Column is full

def place_checker(board, row_idx, col_idx, checker):
    # Place the player's checker on the board
    board[row_idx][col_idx] = checker

def check_win(board, checker):
    # Check for win in all directions
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal (\) check
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal (/) check
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def check_draw(board):
    # True if every column is full
    return all(board[0][c] != " " for c in range(COLS))

def get_player_input(board, player_idx):
    # Prompt for valid input for this player
    checker = PLAYER_CHECKERS[player_idx]
    while True:
        col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        if not is_valid_column_choice(col_input):
            print("Invalid input: Please enter a valid column letter.")
            continue
        col_idx = get_column_index(col_input)
        if is_column_full(board, col_idx):
            print("Column is full: You lose your turn.")
            return None  # Column full: lose turn
        return col_idx

def main():
    board = create_board()
    # Choose first player randomly
    current_player = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    game_over = False

    while not game_over:
        checker = PLAYER_CHECKERS[current_player]
        col_idx = get_player_input(board, current_player)
        clear_screen()
        if col_idx is None:
            # Lose the turn, move to next player
            print_board(board)
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_idx = get_next_open_row(board, col_idx)
        place_checker(board, row_idx, col_idx, checker)
        print_board(board)

        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
            continue
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            continue
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
