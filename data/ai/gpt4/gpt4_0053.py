import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # ['A', 'B', 'C', ...]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == " "

def drop_checker(column, checker, board):
    col_index = COLUMN_LABELS.index(column)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical, diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4))) or \
               (col + 3 < COLUMNS and row + 3 < ROWS and all(board[row + i][col + i] == checker for i in range(4))) or \
               (col - 3 >= 0 and row + 3 < ROWS and all(board[row + i][col - i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_column(column, board):
            print("Invalid input. Try again.")
            continue
        
        drop_checker(column, player_checker, board)
        print_board(board)
        
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw.")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
