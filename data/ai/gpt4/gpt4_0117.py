import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_valid_column(board):
    while True:
        col_input = input("Enter a column: ").strip().upper()
        if len(col_input) == 1 and "A" <= col_input < chr(65 + COLS):
            col = ord(col_input) - 65
            if board[0][col] == " ":
                return col
        print("Invalid input. Try again.")

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row

def check_win(board, row, col, checker):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in (-1, 1):
            r, c = row, col
            while True:
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    break
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}'s turn.")
        col = get_valid_column(board)
        row = drop_checker(board, col, CHECKERS[current_player])
        print_board(board)

        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
