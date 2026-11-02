import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1):
            return ord(col) - 65
        print("Invalid input. Please enter a valid column (A-G).")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if (c + 3 < COLS and all(board[r][c + i] == checker for i in range(4))) or \
               (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))) or \
               (r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col = get_valid_input(current_player)
        if not place_checker(board, col, current_player):
            print("Column is full! Try again.")
            continue
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
