import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2

# Player symbols
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

def initialize_board(rows, columns):
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def check_valid_input(column_choice):
    if column_choice.isalpha() and column_choice.isupper() and ord(column_choice) - 65 < COLUMNS:
        return True
    return False

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col+i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    current_player_idx = random.choice(range(MAX_PLAYERS))
    
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            column_choice = input().strip()
            if check_valid_input(column_choice):
                column_idx = ord(column_choice) - 65
                if place_checker(board, column_idx, current_checker):
                    break
                else:
                    print("Column is full. Try another column.")
            else:
                print("Invalid input. Please enter a valid column.")

        print_board(board)

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print("Game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
