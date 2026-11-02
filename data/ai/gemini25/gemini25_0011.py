import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


# --- HELPER FUNCTIONS ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def get_column_letter(col_index):
    """Converts a column index (0-25) to its corresponding uppercase letter (A-Z)."""
    if 0 <= col_index < 26:
        return chr(ord('A') + col_index)
    return None


def get_column_index(col_letter):
    """Converts an uppercase column letter (A-Z) to its corresponding index (0-25)."""
    if len(col_letter) == 1 and 'A' <= col_letter <= 'Z':
        return ord(col_letter) - ord('A')
    return -1


def initialize_board(rows, cols):
    """
    Initializes a new Connect 4 board with the given dimensions.
    All cells are initialized with whitespace.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print('  ', end='')
    for i in range(num_cols):
        print(f'{get_column_letter(i)}   ', end='')
    print()

    # Print board content
    for r in range(num_rows):
        print('+---' * num_cols + '+')
        print('|', end='')
        for c in range(num_cols):
            print(f' {board[r][c]} |', end='')
        print()
    print('+---' * num_cols + '+')


def get_player_input(player_name, board):
    """
    Prompts the current player for a column choice and validates the input.
    Continues to ask until valid input is received.
    """
    num_cols = len(board[0])

    while True:
        col_input = input(f"Player {player_name}, please enter a column: ").upper()

        if len(col_input) != 1 or not ('A' <= col_input <= get_column_letter(num_cols - 1)):
            print(f"Invalid input. Please enter a single letter from A to {get_column_letter(num_cols - 1)}.")
            continue

        col_index = get_column_index(col_input)

        if board[0][col_index] != ' ':  # Check if the top of the column is full
            print("That column is full. Please choose another column.")
            continue

        return col_index


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was placed, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return True
    return False  # Column is full (should be caught by input validation, but good safeguard)


def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game by connecting 'win_condition' checkers
    horizontally, vertically, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(num_rows - win_condition + 1):
        for c in range(win_condition - 1, num_cols):
            if all(board[r + i][c - i] == player_checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found


def main():
    """
    Main function to run the Connect 4 game.
    """
    if NUM_COLS > 26:
        print("Error: Maximum columns supported is 26 (A-Z). Please adjust NUM_COLS.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5. Please adjust NUM_PLAYERS.")
        sys.exit(1)

    board = initialize_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]  # Select checkers based on NUM_PLAYERS
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    while not game_over:
        current_player_checker = players[current_player_index]

        col_to_drop = get_player_input(current_player_checker, board)

        # Drop checker (input validation already handled column full, so this should always succeed)
        drop_checker(board, col_to_drop, current_player_checker)

        print_board(board)

        # Check for win
        if check_win(board, current_player_checker, WIN_CONDITION):
            winner = current_player_checker
            game_over = True
            break

        # Check for draw
        if check_draw(board):
            game_over = True
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End of game messages
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
