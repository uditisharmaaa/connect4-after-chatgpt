import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Create board with spaces
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board with column labels
def print_board(board):
    os.system('clear')  # Clear the screen
    print('  ' + '   '.join(chr(c) for c in range(ord('A'), ord('A') + COLS)))
    print('+' + ('---+' * COLS))
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + ('---+' * COLS))

# Validate user input
def validate_input(input_char):
    if len(input_char) == 1 and 'A' <= input_char <= chr(ord('A') + COLS - 1):
        return True
    return False

# Place checker in correct position
def place_checker(board, player_symbol, column):
    col_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player_symbol
            return True
    return False

# Check for a win condition
def check_win(board, player_symbol):
    # Check horizontal, vertical and diagonal
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player_symbol:
                for dr, dc in directions:
                    if all(0 <= r + dr*n < ROWS and 0 <= c + dc*n < COLS and board[r + dr*n][c + dc*n] == player_symbol for n in range(4)):
                        return True
    return False

# Check for draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect_4():
    # Initialize board
    board = create_board()
    print_board(board)

    # Randomly select first player
    current_player_index = random.randint(0, MAX_PLAYERS - 1)

    while True:
        current_symbol = PLAYERS_SYMBOLS[current_player_index]
        player_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()

        # Validate input
        if not validate_input(player_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        # Attempt to place checker
        if not place_checker(board, current_symbol, player_input):
            print("Column full. Turn lost.")
            current_player_index = (current_player_index + 1) % MAX_PLAYERS
            continue

        print_board(board)
        
        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate player
        current_player_index = (current_player_index + 1) % MAX_PLAYERS

connect_4()
