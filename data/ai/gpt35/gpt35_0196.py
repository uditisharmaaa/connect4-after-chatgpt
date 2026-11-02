import os
import random
import string

# Constants for the game
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4

# Player checkers in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Valid column letters for current COLUMNS
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    horizontal_line = "+" + "---+" * len(board[0])
    for row in board:
        print(horizontal_line)
        print("| " + " | ".join(row) + " |")
    print(horizontal_line)

def get_valid_column_from_player(player_checker):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Validate input: must be a single letter in COLUMN_LABELS
        if len(col_input) != 1 or col_input not in COLUMN_LABELS:
            print(f"Invalid input. Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        return col_input

def place_checker(board, col_letter, checker):
    col_idx = COLUMN_LABELS.index(col_letter)
    # Place checker at the lowest available row (from bottom up)
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    # Column full, lose turn
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == WIN_COUNT:
                    return True
            else:
                count = 0

    # Check diagonal (bottom-left to top-right)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                # Check diagonal up-right
                if r - (WIN_COUNT -1) >= 0 and c + (WIN_COUNT -1) < cols:
                    if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                        return True
                # Check diagonal down-right
                if r + (WIN_COUNT -1) < rows and c + (WIN_COUNT -1) < cols:
                    if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                        return True
    return False

def check_draw(board):
    # If no cell is empty, it's a draw
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col_letter = get_valid_column_from_player(current_checker)
        placed = place_checker(board, col_letter, current_checker)
        clear_screen()
        print_board(board)
        if not placed:
            # Column full => lose turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        # Check win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break
        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
