import os
import random

# Constants for board dimensions and game settings
ROWS = 6                # Number of rows in the board
COLS = 7                # Number of columns in the board (max 26)
NUM_PLAYERS = 2         # Number of players (between 2 and 5)
WIN_COUNT = 4           # Number of connected checkers needed to win
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Create an empty board with given rows and columns.
    Each cell initialized with a whitespace " ".
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Print the board to the screen with column labels (A, B, C, ...)
    and rows with separators as per assignment example.
    """
    clear_screen()
    cols = len(board[0])
    # Print column headers
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    # Print the rows with lines
    row_sep = '+' + '---+' * cols
    for row in board:
        print(row_sep)
        row_line = '| ' + ' | '.join(row) + ' |'
        print(row_line)
    print(row_sep)

def valid_column_input(user_input, cols):
    """
    Check if user input is a valid column letter (A up to the max column).
    """
    if len(user_input) != 1:
        return False
    letter = user_input.upper()
    return 'A' <= letter < chr(ord('A') + cols)

def column_index_from_letter(letter):
    """Convert column letter (A, B, C, ...) to zero-based index."""
    return ord(letter.upper()) - ord('A')

def place_checker(board, col, checker):
    """
    Place the checker in the specified column on the lowest available spot.
    If the column is full, return False indicating invalid move.
    Otherwise place checker and return True.
    """
    rows = len(board)
    # Start from the bottom row up
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # Column full

def board_full(board):
    """Return True if the board is completely full."""
    # If any cell in top row is empty, board is not full
    return all(cell != ' ' for cell in board[0])

def check_winner(board, checker):
    """
    Check the board for a win by this checker.
    A win is 4 consecutive checkers horizontally,
    vertically, or diagonally (in both directions).
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - (WIN_COUNT - 1)):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - (WIN_COUNT - 1)):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (down-right) check
    for r in range(rows - (WIN_COUNT - 1)):
        for c in range(cols - (WIN_COUNT - 1)):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (up-right) check
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - (WIN_COUNT - 1)):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Select players' checkers in order for enabled players
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select a player to start
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, please enter a column:")

        while True:
            user_input = input().strip().upper()
            # Validate input format
            if not valid_column_input(user_input, COLS):
                print(f"Invalid input. Please enter a single letter A-{chr(ord('A') + COLS -1)}:")
                continue
            col = column_index_from_letter(user_input)
            # Try to place checker in the column
            if not place_checker(board, col, player_checker):
                # Column full: turn lost
                print(f"Column {user_input} is full. Turn lost.")
                break  # Exit input loop and lose turn
            else:
                # Successfully placed checker
                break

        print_board(board)

        # Check for win condition (only if checker was placed)
        # If column was full and turn lost (no 'place_checker' success), then skip this check
        # We can detect that because we either broke after placing
        if board_full(board):
            print("The game is a draw!")
            break

        # Check for winner only if last move placed checker successfully
        # We can determine success because if turn lost, break below was called before placing
        # We'll check the winner anyway, because if an invalid move was made, turn is lost,
        # checker was not placed. So we can check only if checker was placed.
        # Our code places checker only on success.
        # Because no variable is stored in place_checker about success, track via above flow:
        # Actually, we break out of input loop once placed or full. If full, no checker placed.
        # To handle this, we can check if last move put checker in board or not.
        # The simplest way: check winner only if column was not full (checker placed).
        # So let's do that by remembering that if checker placed the inner loop ended via break,
        # otherwise continue was called.
        # Since after input loop ends we do not have explicit info => alternative:
        # Let's redesign to return success flag from place_checker and act accordingly.

        # Let's adjust code: move place_checker outside loop and retry input if invalid 
        # but lose turn if column full. 
        # We'll implement it now properly.

        # So we need to rewrite input loop to handle turn loss logic properly.

        # Let's break the current logic by reimplementing the input loop here:

        # Redesign:
        # Prompt user until valid input (valid column letter). 
        # If column full, print message and lose turn (break input loop without placing).
        # Else place and break input loop.

        # That was what we implemented.

        # So if checker is placed, check winner.
        # Else if turn lost because column full, don't check winner, just continue with next player.

def run_game():
    # Helper main with correct flow for input and placing

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        print(f"Player {player_checker}, please enter a column:")

        # Input and placing loop: keep asking for input until valid input and try place
        # If column full, lose turn, do not ask again
        placed = False
        while True:
            user_input = input().strip().upper()
            if not valid_column_input(user_input, COLS):
                print(f"Invalid input. Please enter a single letter A-{chr(ord('A') + COLS -1)}:")
                continue
            col = column_index_from_letter(user_input)
            if not place_checker(board, col, player_checker):
                print(f"Column {user_input} is full. Turn lost.")
                placed = False
                break  # lose turn
            else:
                placed = True
                break  # placed successfully

        print_board(board)

        # Check for win if checker placed
        if placed:
            if check_winner(board, player_checker):
                print(f"Player {player_checker} won!")
                break

        # Check for draw after any move (placed or not)
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    run_game()
