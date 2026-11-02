import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Max 5 players as per spec
WIN_CONDITION = 4
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(col):
    return col in COLUMN_LABELS

def get_column_index(col):
    return COLUMN_LABELS.index(col)

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    """
    Place checker in the specified column if possible.
    The checker falls to the lowest available row in that column.
    If column is full, return False. Otherwise True.
    """
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal right-down check
    for r in range(ROWS - WIN_CONDITION + 1):
        for c in range(COLUMNS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Diagonal left-down check
    for r in range(ROWS - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def get_player_input(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not col:
            continue
        if not is_valid_column(col):
            # Invalid column letter
            continue
        col_idx = get_column_index(col)
        return col_idx

def main():
    board = create_board(ROWS, COLUMNS)

    players = CHECKERS[:NUM_PLAYERS]
    # Select random starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    print_board(board)

    while True:
        checker = players[current_player_idx]

        # Get user input; validate input column
        while True:
            col_idx = get_player_input(checker)
            # Check if column full
            if is_column_full(board, col_idx):
                # player loses turn if column full
                break
            else:
                # Place checker and exit input loop
                place_checker(board, col_idx, checker)
                break

        print_board(board)

        # Check if last move was valid and placed (if column full, no checker placed)
        if not is_column_full(board, col_idx) or board[0][col_idx] != " ":
            # Check for win
            if check_win(board, checker):
                print(f"Player {checker} won!")
                return

            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                return

        # Cycle to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
