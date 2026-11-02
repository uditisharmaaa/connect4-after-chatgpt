import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def is_valid_input(col_input):
    return col_input.isalpha() and len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + COLS - 1)

def get_valid_column(board):
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if is_valid_input(col_input):
            col_index = ord(col_input) - ord('A')
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full! Try another column.")
        else:
            print("Invalid input! Please enter a valid column (A-G).")

def place_checker(board, col_index, player_piece):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player_piece
            return True
    return False

def check_win(board, player_piece):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player_piece for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_piece for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_piece for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_piece for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game loop
board = create_board()
current_player_index = random.randint(0, len(PLAYER_PIECES) - 1)
game_over = False

clear_screen()
print_board(board)

while not game_over:
    current_player = PLAYER_PIECES[current_player_index]
    col_index = get_valid_column(board)
    place_checker(board, col_index, current_player)

    clear_screen()
    print_board(board)

    if check_win(board, current_player):
        print(f"Player {current_player} won!")
        game_over = True
    elif check_draw(board):
        print("The game is a draw!")
        game_over = True
    else:
        current_player_index = (current_player_index + 1) % len(PLAYER_PIECES)
