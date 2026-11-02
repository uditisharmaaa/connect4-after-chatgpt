import os
import random

# Constants
MAX_COLUMNS = 26
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Only first NUM_PLAYERS are used

# Initialize the board
def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join(chr(65+i) for i in range(len(board[0]))))
    # Print board
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical, and diagonal wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_line(board, checker, row, col, 0, 1) or   # Horizontal
                check_line(board, checker, row, col, 1, 0) or   # Vertical
                check_line(board, checker, row, col, 1, 1) or   # Diagonal /
                check_line(board, checker, row, col, 1, -1)):  # Diagonal \
                return True
    return False

# Helper function to check lines for win
def check_line(board, checker, start_row, start_col, d_row, d_col):
    count = 0
    for i in range(4):
        row = start_row + i * d_row
        col = start_col + i * d_col
        if 0 <= row < ROWS and 0 <= col < COLUMNS and board[row][col] == checker:
            count += 1
        else:
            break
    return count == 4

# Check for a draw
def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Get valid move from player
def get_valid_move(player):
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(move) == 1 and 'A' <= move <= 'G':
            col = ord(move) - ord('A')
            if any(board[row][col] == ' ' for row in range(ROWS)):
                return col
            else:
                print("Column is full. Choose another one.")
        else:
            print("Invalid input. Please enter a valid column.")

# Place a checker on the board
def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            break

# Main game loop
def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    player_order = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    print_board(board)
    
    while True:
        current_player = player_order[current_player_index]
        col = get_valid_move(current_player)
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
