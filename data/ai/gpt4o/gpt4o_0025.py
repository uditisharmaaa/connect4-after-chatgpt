import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Extend this if the number of players increases

def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65+i) for i in range(len(board[0])))  # Column labels A, B, C, ...
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    return column.isalpha() and ord(column.upper()) - 65 < len(board[0])

def drop_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal wins
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == checker:
                # Check horizontal
                if col <= len(board[0]) - 4 and all(board[row][col+i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row <= len(board) - 4 and all(board[row+i][col] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if row <= len(board) - 4 and col <= len(board[0]) - 4 and all(board[row+i][col+i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if row <= len(board) - 4 and col >= 3 and all(board[row+i][col-i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_index]
        column = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        
        if not is_valid_column(column, board):
            print("Invalid column. Try again.")
            continue
        
        if not drop_checker(board, column, current_checker):
            print(f"Column {column} is full. You lose your turn.")
        else:
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
