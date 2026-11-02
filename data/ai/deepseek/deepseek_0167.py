import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    # Print column headers
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def get_valid_column():
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(user_input) == 1 and user_input.isalpha():
            col = ord(user_input) - ord('A')
            if 0 <= col < COLS:
                if is_valid_move(board, col):
                    return col
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid column. Please enter a letter within the board range.")
        else:
            print("Invalid input. Please enter a single letter (A-G).")

# Initialize the game
board = initialize_board()
current_player = random.randint(0, PLAYERS-1)
players_checkers = CHECKERS[:PLAYERS]

print_board(board)

# Game loop
while True:
    col = get_valid_column()
    place_checker(board, col, players_checkers[current_player])
    print_board(board)
    
    if check_win(board, players_checkers[current_player]):
        print(f"Player {players_checkers[current_player]} won!")
        break
    
    if is_draw(board):
        print("The game is a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
