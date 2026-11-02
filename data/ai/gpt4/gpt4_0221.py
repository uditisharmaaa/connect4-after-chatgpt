import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"][:2]  # Set to 2 players for submission

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column, board):
    return column.isalpha() and column.upper() in [chr(65 + i) for i in range(COLS)] and not is_column_full(column, board)

def is_column_full(column, board):
    col_idx = ord(column.upper()) - 65
    return board[0][col_idx] != " "

def drop_checker(board, col, checker):
    col_idx = ord(col.upper()) - 65
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            break

def is_winner(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column = input().strip()
        
        if not is_valid_column(column, board):
            print("Invalid input. Try again.")
            input("Press Enter to continue...")
            continue
        
        drop_checker(board, column, current_player)

        if is_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
