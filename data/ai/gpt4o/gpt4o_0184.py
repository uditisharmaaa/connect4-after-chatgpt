import random
import os

# Constants
EMPTY_CELL = ' '
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this for more players
NUM_ROWS = 6
NUM_COLUMNS = 7

# Initialize the board
def initialize_board():
    return [[EMPTY_CELL for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(NUM_COLUMNS)))
    print("+---" * NUM_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLUMNS + "+")

# Check for a win
def check_for_win(board, symbol):
    # Check horizontal, vertical, and diagonal wins
    def check_line(start_row, start_col, delta_row, delta_col):
        count = 0
        row, col = start_row, start_col
        while 0 <= row < NUM_ROWS and 0 <= col < NUM_COLUMNS:
            if board[row][col] == symbol:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += delta_row
            col += delta_col
        return False
    
    # Check all horizontal lines
    for row in range(NUM_ROWS):
        if check_line(row, 0, 0, 1):
            return True
    
    # Check all vertical lines
    for col in range(NUM_COLUMNS):
        if check_line(0, col, 1, 0):
            return True
    
    # Check diagonal lines (\ direction and / direction)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS):
            if check_line(row, col, 1, 1) or check_line(row, col, -1, 1):
                return True
    
    return False

# Check for a draw
def check_for_draw(board):
    return all(cell != EMPTY_CELL for row in board for cell in row)

# Drop a checker into a column
def drop_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == EMPTY_CELL:
            row[column] = symbol
            return True
    return False

# Get valid column input from the user
def get_valid_column(board):
    while True:
        column_input = input("Please enter a column: ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + NUM_COLUMNS - 1):
            column = ord(column_input) - ord('A')
            if board[0][column] == EMPTY_CELL:
                return column
        print("Invalid input. Please enter a valid column.")

# Main game loop
def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        current_player_symbol = player_symbols[current_player_index]
        print(f"Player {current_player_symbol}, it's your turn.")
        
        column = get_valid_column(board)
        if drop_checker(board, column, current_player_symbol):
            print_board(board)
            
            if check_for_win(board, current_player_symbol):
                print(f"Player {current_player_symbol} won!")
                break
            
            if check_for_draw(board):
                print("The game is a draw.")
                break
            
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
