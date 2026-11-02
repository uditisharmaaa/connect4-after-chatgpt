import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def init_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(input, cols):
    return input.isalpha() and 'A' <= input <= chr(ord('A') + cols - 1)

def place_checker(board, col, player_symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player_symbol
            return True
    return False

def check_win(board, player_symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(cell == player_symbol for cell in board[row][col:col + 4]):
                return True
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player_symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = init_board(ROWS, COLS)
    player_count = 2
    current_player = random.randint(0, player_count - 1)
    player_symbols = PLAYER_SYMBOLS[:player_count]
    
    print_board(board)
    
    while True:
        print(f"Player {player_symbols[current_player]}, please enter a column:")
        user_input = input().strip().upper()
        
        if not is_valid_input(user_input, COLS):
            print("Invalid input! Please enter a valid column letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if not place_checker(board, col, player_symbols[current_player]):
            print("Column full! You lose your turn.")
        else:
            print_board(board)
            if check_win(board, player_symbols[current_player]):
                print(f"Player {player_symbols[current_player]} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % player_count

play_game()
