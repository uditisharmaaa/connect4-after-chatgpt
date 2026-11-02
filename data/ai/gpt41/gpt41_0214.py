import os
import random

# ---- Constants ----
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # Max columns we support (A-Z)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
NUM_PLAYERS = 2  # For this assignment, should be 2

# ---- Board Operations ----
def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board, cols):
    os.system('clear')
    col_labels = [chr(ord('A')+i) for i in range(cols)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+"*cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+"*cols)

# ---- Input Validations ----
def get_col_input(current_player, cols):
    valid_cols = [chr(ord('A')+i) for i in range(cols)]
    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_cols:
            print(f"Invalid input. Choose a letter between {valid_cols[0]} and {valid_cols[-1]}.")
            continue
        return valid_cols.index(inp)

# ---- Game Logic ----
def place_checker(board, col, checker):
    # Place checker at bottom-most available row in the given column.
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full

def check_win(board, num_to_win, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for row in range(rows):
        for col in range(cols - num_to_win + 1):
            if all(board[row][col+i] == checker for i in range(num_to_win)):
                return True

    # Vertical
    for col in range(cols):
        for row in range(rows - num_to_win + 1):
            if all(board[row+i][col] == checker for i in range(num_to_win)):
                return True

    # Diagonal (\)
    for row in range(rows - num_to_win + 1):
        for col in range(cols - num_to_win + 1):
            if all(board[row+i][col+i] == checker for i in range(num_to_win)):
                return True

    # Diagonal (/)
    for row in range(num_to_win-1, rows):
        for col in range(cols - num_to_win + 1):
            if all(board[row-i][col+i] == checker for i in range(num_to_win)):
                return True

    return False

def check_draw(board):
    # If no spaces left in top row, board is full
    return all(cell != " " for cell in board[0])

# ---- Main Game Function ----
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS-1)
    print_board(board, NUM_COLS)
    print(f"Player {checkers[current]} will start!\n")

    while True:
        print_board(board, NUM_COLS)
        col = get_col_input(checkers[current], NUM_COLS)
        placed_row = place_checker(board, col, checkers[current])

        if placed_row == -1:
            print("Column is full. You lose your turn.")
        else:
            # Check for win
            if check_win(board, 4, checkers[current]):
                print_board(board, NUM_COLS)
                print(f"Player {checkers[current]} won!")
                break
            # Check for draw
            if check_draw(board):
                print_board(board, NUM_COLS)
                print("It's a draw!")
                break
        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
