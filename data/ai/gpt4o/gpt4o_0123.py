import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Initialize the game board as a list of lists, with spaces representing empty slots."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board to the console."""
    os.system('clear')  # Clear the terminal
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')

def is_valid_input(input_char, cols):
    """Check if the input is a valid column selection."""
    return input_char.isalpha() and 'A' <= input_char < chr(ord('A') + cols)

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check if there is a winner on the board."""
    # Check horizontal, vertical, and diagonal alignments for a win
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                if (
                    check_direction(board, row, col, 1, 0, checker) or  # Horizontal
                    check_direction(board, row, col, 0, 1, checker) or  # Vertical
                    check_direction(board, row, col, 1, 1, checker) or  # Diagonal /
                    check_direction(board, row, col, 1, -1, checker)   # Diagonal \
                ):
                    return True
    return False

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    """Check 4 checkers in one direction."""
    for step in range(1, 4):  # Look for 3 additional checkers
        new_row = start_row + step * delta_row
        new_col = start_col + step * delta_col
        if (
            not (0 <= new_row < ROWS and 0 <= new_col < COLS) or
            board[new_row][new_col] != checker
        ):
            return False
    return True

def check_draw(board):
    """Check if the board is fully occupied, leading to a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game(num_players):
    """Execute the Connect 4 game loop."""
    board = create_board(ROWS, COLS)
    current_player = random.choice(range(num_players))
    print_board(board)

    while True:
        current_checker = PLAYER_CHECKERS[current_player]
        user_input = input(f"Player {current_checker}, please enter a column: ").upper()

        if is_valid_input(user_input, COLS):
            col = ord(user_input) - ord('A')
            if place_checker(board, col, current_checker):
                print_board(board)
                if check_winner(board, current_checker):
                    print(f"Player {current_checker} won!")
                    break
                if check_draw(board):
                    print("The game is a draw!")
                    break
                current_player = (current_player + 1) % num_players  # Alternate turns
            else:
                print("Column full. Turn skipped.")
        else:
            print("Invalid input, please select a valid column.")

if __name__ == "__main__":
    play_game(2)
