import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print("  " + "   ".join([chr(65 + i) for i in range(BOARD_COLS)]))
    print("+---" * BOARD_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * BOARD_COLS + "+")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def get_valid_input():
    while True:
        # Player enters input
        player_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if len(player_input) == 1 and 'A' <= player_input <= chr(64 + BOARD_COLS):
            column = ord(player_input) - 65
            if board[0][column] == " ":
                return column
            else:
                print("Column is full. Try another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
                
    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, BOARD_COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
                
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game(board, num_players):
    global current_player
    current_player = random.randint(0, num_players - 1)
    print_board(board)
    
    while True:
        column = get_valid_input()
        place_checker(board, column, CHECKERS[current_player])
        print_board(board)
        
        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % num_players

# Initialize game parameters and board
num_players = 2
board = create_board(BOARD_ROWS, BOARD_COLS)
play_game(board, num_players)
