import os
import random
import string

# ==============================
# Constants
# ==============================
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # For generalization, not used here
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# ==============================
# Helper Functions
# ==============================

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(COLUMNS)]
    print("  ", "   ".join(headers))
    print("+" + "---+" * COLUMNS)
    for row in range(ROWS):
        print("| " + " | ".join(board[row]) + " |")
        print("+" + "---+" * COLUMNS)

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def get_player_checkers(count):
    return CHECKERS[:count]

def is_valid_column(col, board):
    if len(col) != 1 or col not in string.ascii_uppercase[:COLUMNS]:
        return False
    idx = string.ascii_uppercase.index(col)
    # If top of column is not empty, it's full
    return board[0][idx] == " "

def place_checker(board, column, checker):
    col_idx = string.ascii_uppercase.index(column)
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx  # Return position for win-checking
    return None  # Should not happen if validated before

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def check_winner(board, player_checker):
    # Check horizontal, vertical, and both diagonals for 4 in a row
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player_checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player_checker for i in range(4)):
                return True

    # Diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player_checker for i in range(4)):
                return True

    # Diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player_checker for i in range(4)):
                return True
    return False

# ==============================
# Main Game Loop
# ==============================

def main():
    board = create_board()
    player_checkers = get_player_checkers(PLAYER_COUNT)
    players = [f"Player {c}" for c in player_checkers]
    current_player = random.randint(0, PLAYER_COUNT - 1)

    print_board(board)
    input(f"{players[current_player]} ({player_checkers[current_player]}) will start! Press Enter to start the game...")

    winner = None
    while True:
        print_board(board)
        print()
        player_name = players[current_player]
        player_marker = player_checkers[current_player]
        move_ok = False
        while not move_ok:
            inp = input(f"{player_name} ({player_marker}), please enter a column: ").strip().upper()
            if not is_valid_column(inp, board):
                print("Invalid input. Please enter a valid column letter (A-G), not full, and only one letter.")
                continue
            move_ok = True

        row_col = place_checker(board, inp, player_marker)
        # Check for win and draw
        if check_winner(board, player_marker):
            print_board(board)
            print(f"{player_name} ({player_marker}) won!")
            winner = current_player
            break
        elif board_full(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
