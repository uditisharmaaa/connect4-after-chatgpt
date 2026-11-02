import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  ", "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(input_str):
    return input_str in COLUMN_LABELS

def find_lowest_empty_row(board, col_index):
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            return row
    return -1

def place_checker(board, col_index, checker):
    row_index = find_lowest_empty_row(board, col_index)
    if row_index != -1:
        board[row_index][col_index] = checker
        return True
    return False

def check_win(board, checker):
    def check_direction(x, y, dx, dy):
        count = 0
        for step in range(4):
            nx, ny = x + step * dx, y + step * dy
            if 0 <= nx < ROWS and 0 <= ny < COLUMNS and board[nx][ny] == checker:
                count += 1
            else:
                break
        return count == 4
    
    for x in range(ROWS):
        for y in range(COLUMNS):
            if board[x][y] == checker:
                if (check_direction(x, y, 1, 0) or  # Horizontal
                    check_direction(x, y, 0, 1) or  # Vertical
                    check_direction(x, y, 1, 1) or  # Diagonal /
                    check_direction(x, y, 1, -1)): # Diagonal \
                    return True
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = initialize_board()
    current_player = random.choice(CHECKERS)
    while True:
        print_board(board)
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if not is_valid_input(col_input):
            print("Invalid input, try again.")
            continue
        
        col_index = COLUMN_LABELS.index(col_input)
        
        if not place_checker(board, col_index, current_player):
            print("Column full, you lose your turn.")
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]

if __name__ == '__main__':
    main()
