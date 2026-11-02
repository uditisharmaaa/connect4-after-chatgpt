import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows with '+' and '|' formatting
    line = "+" + "---+" * COLS
    for row in board:
        print(line)
        print("| " + " | ".join(row) + " |")
    print(line)

def is_valid_column(col_label):
    return col_label in COLUMN_LABELS

def column_index(col_label):
    return ord(col_label) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker's piece in the lowest available spot in the column.
    Returns True if placed, False if column full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True
    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - WIN_LENGTH + 1):
            if all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal (down-right) check
    for r in range(ROWS - WIN_LENGTH + 1):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_LENGTH)):
                return True
    # Diagonal (up-right) check
    for r in range(WIN_LENGTH - 1, ROWS):
        for c in range(COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def get_player_input(player_checker):
    """
    Prompts player to enter a column letter.
    Validates input to be uppercase letter in range,
    excluding full column.
    Returns the valid column index or None if column full.
    Repeats until valid input or column full.
    """
    while True:
        col_label = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(col_label) != 1 or not col_label.isalpha():
            print(f"Invalid input. Please enter a single uppercase letter from A to {COLUMN_LABELS[-1]}.")
            continue
        col_label = col_label.upper()
        if not is_valid_column(col_label):
            print(f"Invalid column. Please enter a letter from A to {COLUMN_LABELS[-1]}.")
            continue
        col = column_index(col_label)
        return col

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = players[current_player_idx]
        # Input and place checker
        col = get_player_input(player_checker)
        placed = place_checker(board, col, player_checker)
        if not placed:
            # Column full, player loses turn
            # As per assignment: "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn."
            # So we just skip placing and move to next player.
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue
        print_board(board)
        # Check for win
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        # Check for draw
        if board_full(board):
            print("Game is a draw!")
            break
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
