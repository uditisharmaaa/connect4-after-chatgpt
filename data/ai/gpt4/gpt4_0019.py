import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # Extend to ["X", "O", "V", "H", "M"] for up to 5 players
EMPTY_CELL = " "
COLUMN_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # ['A', 'B', 'C', ..., 'G']

# Create the board
def create_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))
    print("+---" * len(board[0]) + "+")
    # Print board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Validate user input
def is_valid_input(input_str, board):
    return input_str in COLUMN_LABELS[:len(board[0])]

# Drop checker into the selected column
def drop_checker(board, column, checker):
    column_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[column_index] == EMPTY_CELL:
            row[column_index] = checker
            return True
    return False  # If column is full

# Check for a win condition
def check_for_win(board, player):
    # Check horizontal win
    for row in board:
        for col in range(len(row) - 3):
            if all(cell == player for cell in row[col:col + 4]):
                return True

    # Check vertical win
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check if the board is full (draw)
def is_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

# Main game logic
def connect_4():
    # Initialize board and choose random starting player
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        # Prompt for input
        while True:
            user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if is_valid_input(user_input, board):
                if drop_checker(board, user_input, current_player):
                    break
                else:
                    print("Column is full. Choose another column.")
            else:
                print("Invalid input. Please enter a valid column.")

        print_board(board)

        # Check for win
        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Run the game
if __name__ == "__main__":
    connect_4()
