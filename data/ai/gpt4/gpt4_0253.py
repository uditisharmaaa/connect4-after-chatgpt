import os
import random

# Constants
ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def valid_column(col, board):
    return col.isalpha() and len(col) == 1 and "A" <= col <= chr(65 + COLS - 1) and board[0][ord(col.upper()) - 65] == " "

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col

def check_win(board, row, col, checker):
    def count_dir(delta_row, delta_col):
        r, c, count = row, col, 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count - 1

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if count_dir(dr, dc) + count_dir(-dr, -dc) + 1 >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player]
        col = input(f"Player {player_checker}, please enter a column: ").upper()
        while not valid_column(col, board):
            col = input(f"Invalid input. Player {player_checker}, please enter a valid column: ").upper()
        
        col_index = ord(col) - 65
        row, col = drop_checker(board, col_index, player_checker)
        print_board(board)
        
        if check_win(board, row, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
