import os
import random

# Constants for game configuration
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYER_COUNT]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_valid_column(board):
    while True:
        column_input = input("Please enter a column (A-G): ").upper()
        if len(column_input) == 1 and column_input.isalpha():
            column_index = ord(column_input) - 65
            if 0 <= column_index < COLS and board[0][column_index] == " ":
                return column_index
        print("Invalid input. Try again.")

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)
    while True:
        print(f"Player {CHECKERS[current_player_index]}, your turn.")
        column = get_valid_column(board)
        drop_checker(board, column, CHECKERS[current_player_index])
        print_board(board)
        
        if check_win(board, CHECKERS[current_player_index]):
            print(f"Player {CHECKERS[current_player_index]} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    play_game()
