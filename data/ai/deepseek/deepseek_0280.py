import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the screen for Linux/Unix
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print the board rows with separators
    separator = '+' + ('---+' * COLS)
    for row in board:
        print(separator)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print(separator)

def get_valid_column(board):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column > chr(65 + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_index = ord(column) - ord('A')
        if board[0][col_index] != ' ':  # Check if column is full
            print("This column is already full. Please choose another.")
            continue
        return col_index

def place_checker(board, col_index, player):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    global current_player
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col_index = get_valid_column(board)
        place_checker(board, col_index, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
