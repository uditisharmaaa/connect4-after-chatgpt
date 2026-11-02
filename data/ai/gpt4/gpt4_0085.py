import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(65 + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  ", "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(column):
    return column in COLUMN_LABELS

def is_column_full(board, column):
    col_index = COLUMN_LABELS.index(column)
    return board[0][col_index] != " "

def place_checker(board, column, checker):
    col_index = COLUMN_LABELS.index(column)
    for row in range(ROWS - 1, -1, -1):  # Start from bottom
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index

def check_winner(board, row, col, checker):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, \ diagonal, / diagonal
    for dr, dc in directions:
        count = 1
        for step in [-1, 1]:  # check both directions
            r, c = row, col
            for _ in range(3):
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        print(f"Player {players_checkers[current_player]}, please enter a column:")
        column = input().strip().upper()
        
        if not is_valid_column(column):
            print("Invalid column. Try again.")
            continue
        
        if is_column_full(board, column):
            print(f"Column {column} is full. Try again.")
            continue
        
        row, col = place_checker(board, column, players_checkers[current_player])
        print_board(board)
        
        if check_winner(board, row, col, players_checkers[current_player]):
            print(f"Player {players_checkers[current_player]} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
