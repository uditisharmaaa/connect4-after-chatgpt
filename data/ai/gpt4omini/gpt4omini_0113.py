import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Max 5 players can be ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen (Linux/Unix)
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * COLS)

# Check if a column is valid for a move
def is_valid_column(board, column):
    return 0 <= column < COLS and board[0][column] == ' '

# Drop the checker in the specified column
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

# Check for a win in the board
def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game function
def play_game():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        column_input = input(f"Player {current_player}, please enter a column (A-{chr(ord('A') + COLS - 1)}): ").upper()

        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input. Please enter a letter (A-G).")
            continue

        column = ord(column_input) - ord('A')

        if not is_valid_column(board, column):
            print("Column is full or invalid. Try again.")
            continue

        drop_checker(board, column, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]

if __name__ == "__main__":
    play_game()
