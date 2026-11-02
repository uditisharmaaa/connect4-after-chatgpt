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
    return column in (chr(65 + i) for i in range(COLS))

def get_column_index(column):
    return ord(column) - 65

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[get_column_index(column)] == " ":
            row[get_column_index(column)] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):  # Horizontal
                    return True
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):  # Vertical
                    return True
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):  # Diagonal /
                    return True
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):  # Diagonal \
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    random_player = random.choice(PLAYERS)
    current_player = random_player
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()
        
        if not is_valid_input(column):
            print("Invalid input! Please choose a valid column (A-G).")
            continue

        if not drop_checker(board, column, current_player):
            print("Column is full! Please choose another column.")
            continue

        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
