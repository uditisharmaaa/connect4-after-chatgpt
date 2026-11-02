import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'] # First 2 symbols are used for two-player game

# Initialize board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Column Headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    # Board rows
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

# Check if input is valid
def is_valid_input(input_str, board):
    if len(input_str) != 1:
        return False
    col = ord(input_str.upper()) - 65
    return 0 <= col < COLUMNS and board[0][col] == ' '

# Place checker
def place_checker(board, column, symbol):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = symbol
            break

# Check win conditions
def check_win(board, symbol):
    # Check horizontally
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == symbol for cell in row[col:col + 4]):
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Check diagonally (ascending)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True

    # Check diagonally (descending)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True
    
    return False

# Check draw condition
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize board and randomly select first player
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_idx]
        col_input = input(f"Player {current_symbol}, please enter a column: ")

        if not is_valid_input(col_input, board):
            print("Invalid input. Please enter a valid column.")
            continue

        place_checker(board, col_input, current_symbol)
        print_board(board)

        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        # Alternate turns
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
