import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print row content
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print border
        print('+' + ('---+' * COLS))

def get_valid_column(board):
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").upper()
        if len(choice) != 1:
            print("Please enter a single letter.")
            continue
        col = ord(choice) - ord('A')
        if 0 <= col < COLS:
            if board[0][col] == ' ':
                return col
            else:
                print("That column is full. Please choose another.")
        else:
            print(f"Invalid column. Please choose between A and {chr(ord('A') + COLS - 1)}.")

def place_checker(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

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
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize game
board = create_board()
current_player = random.choice(PLAYERS[:NUM_PLAYERS])

# Game loop
while True:
    clear_screen()
    print_board(board)
    
    col = get_valid_column(board)
    place_checker(board, col, current_player)
    
    if check_win(board, current_player):
        clear_screen()
        print_board(board)
        print(f"Player {current_player} won!")
        break
    
    if check_draw(board):
        clear_screen()
        print_board(board)
        print("It's a draw!")
        break
    
    # Switch players
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
