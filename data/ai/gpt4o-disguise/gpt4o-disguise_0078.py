import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O']

# Create board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear') # clear screen
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')

# Validate input
def valid_input(choice, board):
    if choice.isalpha() and len(choice) == 1:
        col = ord(choice.upper()) - ord('A')
        if 0 <= col < COLS and board[0][col] == ' ':
            return True
    return False

# Place checker
def place_checker(col, player_checker, board):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_checker
            break

# Check win
def check_win(board, player_checker):
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c + i] == player_checker for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r + i][c] == player_checker for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player_checker for i in range(4)):
                return True
            if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player_checker for i in range(4)):
                return True
    return False

# Check draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board()
    player_turn = random.randint(0, PLAYERS - 1)
    while True:
        print_board(board)
        print(f"Player {CHECKERS[player_turn]}, please enter a column:")
        choice = input().strip()
        if valid_input(choice, board):
            col = ord(choice.upper()) - ord('A')
            place_checker(col, CHECKERS[player_turn], board)
            if check_win(board, CHECKERS[player_turn]):
                print_board(board)
                print(f"Player {CHECKERS[player_turn]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            player_turn = (player_turn + 1) % PLAYERS
        else:
            print("Invalid input, try again.")

play_game()
