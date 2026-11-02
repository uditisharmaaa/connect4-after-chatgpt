import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_COLUMNS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:COLUMNS]

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(BOARD_COLUMNS[:COLUMNS]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(input_str):
    return input_str in BOARD_COLUMNS[:COLUMNS]

def place_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal lines
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + i][col + 3 - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        
        user_input = input().strip().upper()
        
        if not is_valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column = BOARD_COLUMNS.index(user_input)
        
        if not place_checker(board, column, current_checker):
            print("Column full. Try a different column.")
            continue
        
        print_board(board)
        
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
