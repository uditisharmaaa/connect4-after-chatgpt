import os
import random

# Constants for the board size
ROWS = 6
COLUMNS = 7

# Constants for players and their checkers
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players
NUM_PLAYERS = 2  # Set to 2 for submission as required

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates and returns an empty board with given rows and columns."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board with column labels."""
    clear_screen()
    columns = len(board[0])
    # Print column labels (A, B, C, ...)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(columns))
    print(header)
    # Print the board with gridlines
    sep = "+" + "---+" * columns
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def is_valid_column_input(user_input, columns):
    """Checks if input is a single uppercase letter within the valid columns."""
    if len(user_input) != 1:
        return False
    if not ('A' <= user_input <= chr(ord('A') + columns - 1)):
        return False
    return True

def column_index_from_letter(letter):
    """Converts column letter to column index."""
    return ord(letter) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Places a checker in the given column.
    Returns True if placed successfully, False if the column is full.
    """
    # Traverse from bottom row upwards to find first empty spot
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return True
    return False

def has_winner(board, checker):
    """
    Checks whether the given checker has 4 in a row horizontally,
    vertically or diagonally.
    """
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r][c+1] == checker and
                board[r][c+2] == checker and board[r][c+3] == checker):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == checker and board[r+1][c] == checker and
                board[r+2][c] == checker and board[r+3][c] == checker):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True

    return False

def is_board_full(board):
    """Returns True if board is full (no empty spaces), False otherwise."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        
        # Get valid input for column
        while True:
            user_input = input(prompt).strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter (A-G).")
                continue
            col_idx = column_index_from_letter(user_input)
            # Check if the column is full here - if full, turn lost immediately
            if board[0][col_idx] != " ":
                # Column full, turn lost
                print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                break
            else:
                # Valid column and not full
                placed = place_checker(board, col_idx, current_checker)
                if placed:
                    break
                else:
                    # Should not reach here because we already checked full column,
                    # but just in case:
                    print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                    break
        
        print_board(board)

        # If the checker was placed, check for win
        # If the column was full, player lost turn and we don't check win (since no checker added)
        # We can verify by checking if board[0][col_idx] == current_checker or if the column was full.
        # However, simpler: only check win if checker placed.

        # We know we broke from input loop either after placing checker or losing turn.
        # So check if the bottom cell in col_idx contains current_checker's checker - 
        # this is not a reliable check.
        # Instead, we track placement success via variable; update the code to track placement
        # Modify above to store placement success.

        # To do this cleanly:
        # let's change code above.

    # To handle above, we restructure main loop to better track placement success.

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        placed = False

        # Get valid input and place checker
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if not is_valid_column_input(user_input, COLUMNS):
                print(f"Invalid input. Please enter a letter from A to {chr(ord('A') + COLUMNS - 1)}.")
                continue
            col_idx = column_index_from_letter(user_input)
            if board[0][col_idx] != " ":
                # Column full, turn lost
                print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
                placed = False
                break  # Exit input loop, turn lost
            else:
                # Try to place checker
                placed = place_checker(board, col_idx, current_checker)
                # placed should be True here
                break

        print_board(board)

        if placed:
            # Check for win
            if has_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if is_board_full(board):
                print("The game is a draw!")
                break
        
        # Move to next player turn (even if turn lost)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
