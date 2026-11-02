import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(col, board):
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(65 + COLUMNS - 1) and board[0][ord(col.upper()) - 65] == " "

def drop_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

def check_winner(board, checker):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        
        col = input().strip()
        if is_valid_column(col, board):
            drop_checker(board, col, CHECKERS[current_player])
            if check_winner(board, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
