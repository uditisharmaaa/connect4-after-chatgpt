import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # supports up to 5 players
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))
    # Print rows with separators
    for r in range(rows):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * cols)

def is_valid_column(col_letter, cols):
    if len(col_letter) != 1:
        return False
    if col_letter not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    """
    Place checker in lowest empty row of column col.
    Return True if placed, False if column full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    
    # Helper to safely get cell
    def cell(r, c):
        return board[r][c] if 0 <= r < rows and 0 <= c < cols else None
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(cell(r, c+i) == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(cell(r+i, c) == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-right
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(cell(r+i, c+i) == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal up-right
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(cell(r - i, c + i) == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_player_input(player_checker, cols):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column(inp, cols):
            # Invalid column letter or length
            continue
        col = get_column_index(inp)
        return col

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = players[current_player_idx]

        # Get valid column input:
        col = get_player_input(player_checker, COLUMNS)

        # Try to place checker
        placed = place_checker(board, col, player_checker)
        if not placed:
            # Column full, player loses turn:
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
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
