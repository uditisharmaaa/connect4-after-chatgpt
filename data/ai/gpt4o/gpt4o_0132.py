import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    
    # Print column headers
    headers = "  " + "   ".join([chr(ord('A') + i) for i in range(COLUMNS)]) + "\n"
    print(headers)
    
    # Print board
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def is_valid_input(input_str, columns):
    if len(input_str) != 1:
        return False
    if input_str.isalpha() and 'A' <= input_str <= chr(ord('A') + columns - 1):
        return True
    return False

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def has_winner(board, checker):
    # Check horizontal, vertical and diagonal lines for a win
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True

    # Check diagonal (left bottom to right top)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (left top to right bottom)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        column_letter = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        while not is_valid_input(column_letter, COLUMNS):
            column_letter = input(f"Invalid input. Player {current_checker}, please enter a valid column: ").strip().upper()

        column_index = ord(column_letter) - ord('A')
        
        if not place_checker(board, column_index, current_checker):
            print("Column is full. Turn is lost.")
        else:
            print_board(board)

            if has_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            
            if is_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
