import os
import random

# Constants for the game configuration
ROWS = 6              # Number of rows on the board
COLUMNS = 7           # Number of columns on the board (max 26)
NUM_PLAYERS = 2       # Number of players (2 to 5)
WINNING_LENGTH = 4    # Number of consecutive checkers needed to win

# Players' checker symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates a ROWS x COLUMNS 2D list initialized with spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board with column labels (A through ...) and borders."""
    clear_screen()
    # Print column labels
    labels = "  "
    for i in range(COLUMNS):
        labels += f" {chr(ord('A') + i)}  "
    print(labels)

    # Print the board rows, with borders as shown in example
    horizontal_border = "+" + "---+" * COLUMNS
    for row in range(ROWS):
        print(horizontal_border)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += f" {board[row][col]} |"
        print(row_str)
    print(horizontal_border)

def valid_column_input(user_input):
    """Check if user input is a valid column letter within board range."""
    if len(user_input) != 1:
        return False
    c = user_input.upper()
    if 'A' <= c < chr(ord('A') + COLUMNS):
        return True
    return False

def get_lowest_empty_row(board, col):
    """
    For a given column index, return the index of the lowest empty (from bottom)
    row that checker can occupy. If column is full return -1.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, checker):
    """
    Place the checkers into the given column at the lowest empty row.
    Returns True if placement succeeded, False if the column is full.
    """
    row = get_lowest_empty_row(board, col)
    if row == -1:
        return False
    board[row][col] = checker
    return True

def check_winner(board, checker):
    """
    Check all directions for a sequence of WINNING_LENGTH consecutive
    checker symbols for the given player.
    """
    # Horizontal check
    for row in range(ROWS):
        count = 0
        for col in range(COLUMNS):
            if board[row][col] == checker:
                count += 1
                if count == WINNING_LENGTH:
                    return True
            else:
                count = 0

    # Vertical check
    for col in range(COLUMNS):
        count = 0
        for row in range(ROWS):
            if board[row][col] == checker:
                count += 1
                if count == WINNING_LENGTH:
                    return True
            else:
                count = 0

    # Diagonal checks (top-left to bottom-right)
    for row in range(ROWS - WINNING_LENGTH + 1):
        for col in range(COLUMNS - WINNING_LENGTH + 1):
            count = 0
            for i in range(WINNING_LENGTH):
                if board[row + i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WINNING_LENGTH:
                return True

    # Diagonal checks (bottom-left to top-right)
    for row in range(WINNING_LENGTH - 1, ROWS):
        for col in range(COLUMNS - WINNING_LENGTH + 1):
            count = 0
            for i in range(WINNING_LENGTH):
                if board[row - i][col + i] == checker:
                    count += 1
                else:
                    break
            if count == WINNING_LENGTH:
                return True

    return False

def board_full(board):
    """Returns True if the board has no empty cells, False otherwise."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    # Initialize board
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print initial board
    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        while True:
            user_input = input(prompt).upper()
            if not valid_column_input(user_input):
                # Invalid input: length, not letter or out of range
                print(f"Invalid input. Please enter a column between A and {chr(ord('A') + COLUMNS -1)}.")
                continue

            col = ord(user_input) - ord('A')
            # Check if column is full - if full, player loses turn
            can_place = place_checker(board, col, current_checker)
            if not can_place:
                # Column full: player loses turn, no retry
                break
            else:
                # Valid placement, break input loop to proceed with game check
                break

        print_board(board)

        # If player placed a checker, check for win or draw
        if can_place:
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
