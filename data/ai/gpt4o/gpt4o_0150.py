import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_input(column):
    return len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1)

def get_empty_row(board, column_index):
    for row_index in range(ROWS - 1, -1, -1):
        if board[row_index][column_index] == " ":
            return row_index
    return -1

def make_move(board, column, checker):
    column_index = ord(column) - 65
    row_index = get_empty_row(board, column_index)
    if row_index != -1:
        board[row_index][column_index] = checker
        return True
    return False

def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if all(board[row][col + i] == checker for i in range(4) if col + i < COLUMNS):
                return True
            if all(board[row + i][col] == checker for i in range(4) if row + i < ROWS):
                return True
            if all(board[row + i][col + i] == checker for i in range(4) if row + i < ROWS and col + i < COLUMNS):
                return True
            if all(board[row + i][col - i] == checker for i in range(4) if row + i < ROWS and col - i >= 0):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def connect4():
    board = create_board()
    current_player = random.choice(CHECKERS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_input(column):
            print("Invalid input, please try again.")
            continue
        
        if not make_move(board, column, current_player):
            print("Column is full, you've lost your turn.")
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]
            continue
        
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]

connect4()
