import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))
    print("+---" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLUMNS)

def is_valid_input(column, board):
    if column not in range(COLUMNS):
        return False
    return board[0][column] == " "

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                if r - 3 >= 0 and c + 3 < COLUMNS and all(board[r - i][c + i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    while True:
        print_board(board)
        column_input = input(f"Player {current_player}, please enter a column (A-G): ").strip()
        if len(column_input) != 1 or not('A' <= column_input <= 'G'):
            continue
        
        column = ord(column_input) - 65
        if not is_valid_input(column, board):
            print("Invalid move! Try again.")
            continue
        
        place_checker(board, column, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
