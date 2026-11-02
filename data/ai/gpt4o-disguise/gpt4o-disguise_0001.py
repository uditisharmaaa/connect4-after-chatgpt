import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLS]

# Initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(LETTERS))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

# Get the column index from the player's input
def get_column_input():
    while True:
        col = input("Please enter a column: ").strip().upper()
        if col in LETTERS:
            return LETTERS.index(col)
        print("Invalid column. Please try again.")

# Place a checker in the board
def place_checker(board, checker, col):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for win condition
def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

# Check for draw condition
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    print_board(board)
    player_index = random.randint(0, PLAYERS - 1)
    while True:
        current_checker = CHECKERS[player_index]
        print(f"Player {current_checker},", end=' ')
        col_idx = get_column_input()

        if not place_checker(board, current_checker, col_idx):
            print("Column is full. Turn lost.")
        else:
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        
        player_index = (player_index + 1) % PLAYERS

# Start the game
play_game()
