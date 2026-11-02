import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    os.system('clear')  # Clear the console screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    return column.upper() in [chr(65 + i) for i in range(COLS)]

def get_column_index(column):
    return ord(column.upper()) - 65

def drop_checker(board, column, checker):
    col_index = get_column_index(column)
    for row in reversed(board):  # Start from the bottom row
        if row[col_index] == " ":
            row[col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    def check_direction(start_row, start_col, delta_row, delta_col):
        count = 0
        for i in range(4):
            r = start_row + i * delta_row
            c = start_col + i * delta_col
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
            else:
                break
        return count == 4

    for row in range(ROWS):
        for col in range(COLS):
            if (check_direction(row, col, 0, 1) or  # Horizontal
                check_direction(row, col, 1, 0) or  # Vertical
                check_direction(row, col, 1, 1) or  # Diagonal \
                check_direction(row, col, 1, -1)):  # Diagonal /
                return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(range(len(PLAYERS)))
    
    print_board(board)
    
    while True:
        checker = PLAYERS[current_player]
        column = input(f"Player {checker}, please enter a column: ")

        if is_valid_input(column) and drop_checker(board, column, checker):
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % len(PLAYERS)
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
