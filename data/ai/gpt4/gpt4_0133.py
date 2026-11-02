import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    return column.isalpha() and column.upper() in [chr(65 + i) for i in range(COLUMNS)] and board[0][ord(column.upper()) - 65] == " "

def drop_checker(column, checker, board):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip()
        
        if not is_valid_column(column, board):
            print("Invalid input. Try again.")
            continue
        
        drop_checker(column, CHECKERS[current_player], board)
        print_board(board)
        
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
