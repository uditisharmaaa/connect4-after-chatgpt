import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players
NUM_PLAYERS = 2  # Set to 2 for submission

# Create an empty board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen before printing
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

# Check for a win condition
def has_won(board, symbol):
    # Check horizontally
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == symbol for cell in row[col:col+4]):
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True

    return False

# Check if the game is a draw
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Get the column index from user input
def get_column_index():
    while True:
        col = input(f"Player {player_symbols[current_player]}, please enter a column: ").upper()
        if col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLUMNS - 1):
            return ord(col) - 65
        print("Invalid input, please try again.")

# Place the checker on the board
def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return True
    return False

def connect4():
    board = create_board()
    print_board(board)

    global player_symbols
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Choose a random player to start
    global current_player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        col_index = get_column_index()

        if place_checker(board, col_index, player_symbols[current_player]):
            print_board(board)
            if has_won(board, player_symbols[current_player]):
                print(f"Player {player_symbols[current_player]} won!")
                break
            elif is_draw(board):
                print("The game is a draw!")
                break

            # Alternate to the next player
            current_player = (current_player + 1) % NUM_PLAYERS
        else:
            print("Column full, turn lost!")

if __name__ == '__main__':
    connect4()
