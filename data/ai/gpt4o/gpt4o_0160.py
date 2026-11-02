import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Check for valid input
def is_valid_input(input_column):
    if len(input_column) != 1 or not input_column.isalpha():
        return False
    column_index = ord(input_column.upper()) - 65
    return 0 <= column_index < COLUMNS and board[0][column_index] == ' '

# Place a checker in a column
def place_checker(board, column, checker):
    column_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            break

# Check for a win condition
def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal /
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Main function for game execution
def main():
    global board
    board = create_board()
    print_board(board)

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]

    while True:
        print(f"Player {current_checker}, please enter a column: ", end='')
        input_column = input().strip()

        if not is_valid_input(input_column):
            print("Invalid input. Please enter a valid column.")
            continue

        place_checker(board, input_column, current_checker)
        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]

if __name__ == '__main__':
    main()
