import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # First 2 checkers for 2 players

# Initialize the board with empty spaces
def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join([chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check for valid user input and return the corresponding column
def get_valid_input(board):
    while True:
        input_char = input("Please enter a column: ").upper()
        
        if len(input_char) != 1:
            print("Invalid input, please enter a single letter.")
            continue
        
        column_index = ord(input_char) - ord('A')
        
        if column_index < 0 or column_index >= COLUMNS:
            print("Invalid column, please choose a valid column.")
            continue
        
        # Check if the column is already full
        if board[0][column_index] != ' ':
            print("Column is full, choose another.")
            continue
        
        return column_index

# Place the checker and return the row index where it was placed
def place_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row

# Check if there's a win condition in the board
def check_for_win(board, row, col, checker):
    # Check for horizontal win
    for start_col in range(max(0, col - 3), min(COLUMNS - 3, col + 1)):
        if all(board[row][start_col + i] == checker for i in range(4)):
            return True
    
    # Check for vertical win
    if row <= ROWS - 4:
        if all(board[row + i][col] == checker for i in range(4)):
            return True
    
    # Check for diagonal (bottom-left to top-right) win
    for start in range(-3, 1):
        if 0 <= row - start < ROWS - 3 and 0 <= col + start < COLUMNS - 3:
            if all(board[row - start + i][col + start + i] == checker for i in range(4)):
                return True

    # Check for diagonal (top-left to bottom-right) win
    for start in range(-3, 1):
        if 0 <= row + start < ROWS - 3 and 0 <= col + start < COLUMNS - 3:
            if all(board[row + start + i][col + start + i] == checker for i in range(4)):
                return True
    
    return False

# Check if the board is completely filled
def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    
    # Select a random player to start
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    players = CHECKERS[:PLAYER_COUNT]
    
    while True:
        print(f"Player {players[current_player_index]}, it's your turn")
        column = get_valid_input(board)
        row = place_checker(board, column, players[current_player_index])
        
        print_board(board)
        
        # Check for win
        if check_for_win(board, row, column, players[current_player_index]):
            print(f"Player {players[current_player_index]} won!")
            break
        
        # Check for draw
        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYER_COUNT
    
# Initiate the game
play_game()
