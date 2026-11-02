import random
import os
import string

# ==== CONSTANTS ====
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
NUM_PLAYERS = 2  # Change to 2 before submitting
CHECKERS = ["X", "O", "V", "H", "M"]  # Use in order

# ==== FUNCTIONS ====

def create_board(rows, cols):
    """Create a board initialized with spaces"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board):
    """Print the game board."""
    cols = len(board[0])
    # Print column headers (letters)
    print("  " + "   ".join(string.ascii_uppercase[:cols]))
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    """Return a set of column letters where there is space."""
    valid = set()
    for c in range(len(board[0])):
        if board[0][c] == " ":
            valid.add(string.ascii_uppercase[c])
    return valid

def get_column_index(col_letter, cols):
    """Convert column letter to zero-based index."""
    alphabet = string.ascii_uppercase
    if len(col_letter) != 1 or col_letter not in alphabet[:cols]:
        return None
    return alphabet.index(col_letter)

def ask_column(player_checker, board):
    """Prompt the player to enter a column and validate the input."""
    cols = len(board[0])
    valid_columns = get_valid_columns(board)
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in string.ascii_uppercase[:cols]:
            print(f"Invalid input! Please enter a letter A-{string.ascii_uppercase[cols-1]}")
            continue
        if col not in valid_columns:
            print("Selected column is full. You lose your turn.")
            return None  # Invalid turn - will skip
        return get_column_index(col, cols)

def drop_checker(board, col, checker):
    """Drop the checker into the chosen column if possible."""
    rows = len(board)
    for row in range(rows-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not happen if handled properly

def check_winner(board, checker):
    """Check if player with given checker has won (4 in a row)."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical
    for col in range(cols):
        for row in range(rows - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal (/)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    # Diagonal (\)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is completely filled (draw)."""
    return all(cell != " " for cell in board[0])

def choose_first_player(num_players):
    """Randomly selects the initial player index."""
    return random.randint(0, num_players-1)

# ==== MAIN GAME LOOP ====
def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    current_player = choose_first_player(num_players)
    game_over = False

    clear_screen()
    print_board(board)

    while not game_over:
        checker = checkers[current_player]
        # Show prompt
        print(f"Player {checker}'s turn.")

        # Ask for column and validate
        col_idx = ask_column(checker, board)
        if col_idx is None:
            # Lose turn (selected full column)
            current_player = (current_player + 1) % num_players
            clear_screen()
            print_board(board)
            continue

        # Drop checker
        drop_checker(board, col_idx, checker)
        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, checker):
            print(f"Player {checker} won!")
            game_over = True
            continue

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            continue

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
