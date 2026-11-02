import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

# Initialize board
def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLUMNS)]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

# Check for a win
def check_winner(board, player):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c <= COLUMNS - 4 and all(board[r][c + i] == player for i in range(4))) or \
               (r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4))) or \
               (r <= ROWS - 4 and c <= COLUMNS - 4 and all(board[r + i][c + i] == player for i in range(4))) or \
               (r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == player for i in range(4))):
                return True
    return False

# Check for draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

# Get valid player input
def get_valid_input(board, player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
            if board[0][ord(column) - 65] == ' ':
                return ord(column) - 65
            else:
                print("Column is full. Choose another.")
        else:
            print("Invalid input. Enter a valid column letter.")

# Place checker in board
def place_checker(board, column, checker):
    for r in reversed(range(ROWS)):
        if board[r][column] == ' ':
            board[r][column] = checker
            break

# Main game loop
def play_game():
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        column = get_valid_input(board, CHECKERS[current_player_idx])
        place_checker(board, column, CHECKERS[current_player_idx])
        print_board(board)
        
        if check_winner(board, CHECKERS[current_player_idx]):
            print(f"Player {CHECKERS[current_player_idx]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % PLAYERS

play_game()
