import os
import random

# Constants
ROWS, COLS, MAX_PLAYERS = 6, 7, 2
PLAYERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    col_labels = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {col_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    return column.isalpha() and column.isupper() and \
        ord(column) - 65 < len(board[0]) and any(row[ord(column) - 65] == " " for row in board)

def place_checker(column, player, board):
    col_idx = ord(column) - 65
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = player
            return

def check_winner(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                continue
            if c + 3 < COLS and all(board[r][c] == board[r][c + i] for i in range(4)):  # Horizontal
                return True
            if r + 3 < ROWS and all(board[r][c] == board[r + i][c] for i in range(4)):  # Vertical
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r][c] == board[r + i][c + i] for i in range(4)):  # Diagonal \
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r][c] == board[r + i][c - i] for i in range(4)):  # Diagonal /
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    current_player = random.choice(PLAYERS)
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip()
        if is_valid_column(column, board):
            place_checker(column, current_player, board)
            print_board(board)
            if check_winner(board):
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % MAX_PLAYERS]
        else:
            print("Invalid input, try again.")

if __name__ == "__main__":
    main()
