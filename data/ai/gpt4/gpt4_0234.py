import os
import random

# Constants for the game
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

def clear_screen():
    """Clears the screen using the appropriate command."""
    os.system('clear')

def create_board():
    """Creates the initial game board filled with whitespaces."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(65 + col) for col in range(BOARD_COLS)))
    print("+---" * BOARD_COLS + "+")

    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * BOARD_COLS + "+")

def is_valid_column(board, col):
    """Checks if the provided column is valid and not full."""
    if col < 0 or col >= BOARD_COLS:  # Check column range
        return False
    return board[0][col] == " "  # Check if there's space in the column

def get_next_open_row(board, col):
    """Returns the next open row in the specified column."""
    for row in reversed(range(BOARD_ROWS)):
        if board[row][col] == " ":
            return row
    return None

def drop_checker(board, row, col, checker):
    """Drops the player's checker onto the board at the specified position."""
    board[row][col] = checker

def check_win(board, checker):
    """Checks for a win condition (4-in-a-row horizontally, vertically, or diagonally)."""
    # Horizontal check
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS - 3):
            if board[r][c] == checker and board[r][c + 1] == checker and \
               board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Vertical check
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLS):
            if board[r][c] == checker and board[r + 1][c] == checker and \
               board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Diagonal (positive slope) check
    for r in range(BOARD_ROWS - 3):
        for c in range(BOARD_COLS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and \
               board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Diagonal (negative slope) check
    for r in range(3, BOARD_ROWS):
        for c in range(BOARD_COLS - 3):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and \
               board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (the board is completely filled)."""
    for col in range(BOARD_COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(board, current_player):
    """Prompts the user for their input and validates it."""
    while True:
        try:
            col_letter = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
            if len(col_letter) != 1 or not col_letter.isalpha():
                raise ValueError("Invalid input. Please enter a single letter.")
            col = ord(col_letter) - 65  # Convert letter to column index
            if not is_valid_column(board, col):
                raise ValueError("Invalid column. Please choose a valid column.")
            return col
        except ValueError as e:
            print(e)

def main():
    """Main function to execute the game."""
    # Initialize the game
    board = create_board()
    num_players = min(PLAYERS, len(CHECKERS))
    current_player = random.randint(0, num_players - 1)  # Randomly choose first player
    print_board(board)

    # Game loop
    while True:
        col = get_player_input(board, current_player)
        row = get_next_open_row(board, col)
        drop_checker(board, row, col, CHECKERS[current_player])
        print_board(board)

        # Check for win or draw
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
