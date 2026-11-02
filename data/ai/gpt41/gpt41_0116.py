import os
import random
import string

# --------- Configuration Constants ---------
ROW_COUNT = 6
COL_COUNT = 7
PLAYER_COUNT = 2 # 2-5

CHECKERS = ["X", "O", "V", "H", "M"] # You can support up to 5 players.

COLUMN_LABELS = string.ascii_uppercase[:COL_COUNT]

# --------- Board Utilities ---------
def create_board(rows, cols):
    """Creates and returns an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clears the screen and prints the current state of the board."""
    os.system('clear')  # For Unix / Linux systems
    # Print column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label}  ", end="")
    print()
    # Print separator
    print("+" + "---+" * COL_COUNT)
    # Print board rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COL_COUNT)

def board_full(board):
    """Check if the board is full (draw game)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# --------- Game Logic ---------
def is_valid_column(input_char):
    """Validates if input_char is a valid, in-range column label."""
    return input_char in COLUMN_LABELS

def get_valid_column(board, player_checker):
    """Prompts the player repeatedly for a valid column."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").upper().strip()
        if len(user_input) != 1:
            print("Please enter exactly one letter.")
            continue
        if not is_valid_column(user_input):
            print(f"Invalid column. Enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        col_idx = COLUMN_LABELS.index(user_input)
        if board[0][col_idx] != " ":
            print("That column is full. You lose your turn!")
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    """Place the checker in the lowest available row in given column."""
    for row_idx in reversed(range(ROW_COUNT)):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None, None  # Should not happen if we validated correctly

def four_in_a_row(lst, checker):
    """Helper: returns True if there are 4 consecutive of checker in lst."""
    count = 0
    for val in lst:
        count = count + 1 if val == checker else 0
        if count >= 4:
            return True
    return False

def check_win(board, checker):
    """Checks entire board for 4 checkers in a row belonging to checker"""
    # Horizontal check
    for row in board:
        if four_in_a_row(row, checker):
            return True

    # Vertical check
    for col in range(COL_COUNT):
        column = [board[row][col] for row in range(ROW_COUNT)]
        if four_in_a_row(column, checker):
            return True

    # Diagonal (positive slope)
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (negative slope)
    for row in range(3, ROW_COUNT):
        for col in range(COL_COUNT - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# --------- Main Game Loop ---------
def main():
    board = create_board(ROW_COUNT, COL_COUNT)
    active_players = CHECKERS[:PLAYER_COUNT]
    # Random player starts
    current_player = random.randint(0, PLAYER_COUNT - 1)
    print_board(board)
    print(f"Player {active_players[current_player]} will start the game.")

    game_over = False
    while not game_over:
        print_board(board)
        checker = active_players[current_player]
        col_idx = get_valid_column(board, checker)
        if col_idx is None:
            # Invalid turn (column full): skip to next player
            current_player = (current_player + 1) % PLAYER_COUNT
            continue
        row_idx, _ = place_checker(board, col_idx, checker)

        # Win check
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            game_over = True
            break
        # Draw check
        elif board_full(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
