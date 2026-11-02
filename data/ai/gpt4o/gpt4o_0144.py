import os
import random

# Constants configuration
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Order of players based on number of players

# Initialize game board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the screen first
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column letters A, B, C...
    print("+---" * len(board[0]) + "+")  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Cell contents
        print("+---" * len(row) + "+")  # Row border

# Validate if input column is a valid column
def is_valid_input(input_char, board):
    if len(input_char) != 1:
        return False
    column_index = ord(input_char.upper()) - 65  # Convert letter to column index
    return 0 <= column_index < len(board[0])

# Find the lowest empty position within the column
def get_lowest_empty_row(board, col):
    for i in range(len(board) - 1, -1, -1):
        if board[i][col] == ' ':
            return i
    return None

# Check for a win in the board
def check_win(board, player):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False

# Check if board is full
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(len(board[0])))

# Main function to run the game
def connect_4_game(players, num_rows, num_cols):
    board = create_board(num_rows, num_cols)
    current_player_index = random.randint(0, len(players) - 1)
    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        player_input = input().strip()

        if not is_valid_input(player_input, board):
            print("Invalid input. Try again.")
            continue

        column_index = ord(player_input.upper()) - 65
        row_index = get_lowest_empty_row(board, column_index)

        if row_index is None:
            print("Column full, turn lost.")
            current_player_index = (current_player_index + 1) % len(players)
            continue

        board[row_index][column_index] = current_player
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % len(players)

# Setup and start the game with default configuration
if __name__ == '__main__':
    connect_4_game(PLAYERS[:2], NUM_ROWS, NUM_COLUMNS)  # Submit with 2 players and 6x7 dimension
