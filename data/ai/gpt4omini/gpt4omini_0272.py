import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)
    
def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1)

def column_index(column):
    return ord(column) - 65

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if check_direction(board, r, c, 1, 0, checker) or \
                   check_direction(board, r, c, 0, 1, checker) or \
                   check_direction(board, r, c, 1, 1, checker) or \
                   check_direction(board, r, c, 1, -1, checker):
                    return True
    return False

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    for i in range(4):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    turns = 0
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")
        column = input().upper()

        if not is_valid_input(column):
            print("Invalid input. Please choose a valid column.")
            continue

        col_index = column_index(column)

        if not place_checker(board, col_index, current_player):
            print("Column is full, please choose another column.")
            continue
        
        turns += 1

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player = PLAYERS[turns % len(PLAYERS)]

if __name__ == "__main__":
    main()
