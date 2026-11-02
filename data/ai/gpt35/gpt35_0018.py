import os
import random

# Constants for the game
ROWS = 6                    # Number of rows on the board
COLS = 7                    # Number of columns on the board (max 26)
NUM_PLAYERS = 2             # Number of players (2 to 5)
WIN_LENGTH = 4              # Number of checkers in a row needed to win
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Create a 2D list initialized with spaces representing the empty board.
    Board[row][col], row 0 is top, row ROWS-1 is bottom.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board to the terminal in the required format.
    Columns labeled A.. based on COLS, rows unlabeled.
    """
    # Print the column headers (A, B, C ...)
    col_labels = [chr(ord("A") + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # For each row in the board, print the line with checkers and separators
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(user_input, cols):
    """
    Checks if the user input is a single uppercase letter within board columns.
    """
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    letter = user_input.upper()
    if ord(letter) < ord("A") or ord(letter) >= ord("A") + cols:
        return False
    return True

def get_column_index(user_input):
    """Convert column letter to column index (0-based)."""
    return ord(user_input.upper()) - ord("A")

def place_checker(board, col, checker):
    """
    Place checker in the lowest available row in column `col`.
    Returns True if placed successfully, False if column is full.
    """
    # Start from bottom row and go upwards to find empty space
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """
    Check if the player with 'checker' has won by getting
    4 in a row horizontally, vertically or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row+i][col] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-right (\)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row+i][col+i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal down-left (/)
    for row in range(WIN_LENGTH - 1, rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def board_full(board):
    """
    Returns True if the board is full (no empty spaces), else False.
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Choose random starting player (index)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        current_checker = players[current_player_index]
        # Prompt player input
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip()
            if not is_valid_input(user_input, COLS):
                print("Invalid input. Please enter a valid column letter (e.g. A-G).")
                continue
            col = get_column_index(user_input)
            # Try to place checker in that column
            placed = place_checker(board, col, current_checker)
            if not placed:
                # Column full - player loses turn
                print(f"Column {user_input.upper()} is full. You lose your turn.")
                # Pause shortly so player notices
                input("Press Enter to continue...")
            break

        # If placed successfully, check for winner
        if placed:
            if check_winner(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break

        # If board full and no winner, it's a draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
