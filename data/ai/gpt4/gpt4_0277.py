import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(col, board):
    return col.isalpha() and 65 <= ord(col.upper()) < 65 + COLS and board[0][ord(col.upper()) - 65] == " "

def place_checker(board, col, checker):
    col_idx = ord(col.upper()) - 65
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx, col_idx

def check_winner(board, row, col, checker):
    def count(direction):
        r, c = row, col
        total = 0
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            total += 1
            r, c = r + direction[0], c + direction[1]
        return total

    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        if count((dr, dc)) + count((-dr, -dc)) - 1 >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    player_count = min(PLAYERS, 5)
    players = CHECKERS[:player_count]
    current_player = random.choice(players)

    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        col = input().strip().upper()

        if not is_valid_input(col, board):
            print("Invalid input. Try again.")
            continue

        row, col_idx = place_checker(board, col, current_player)
        print_board(board)

        if check_winner(board, row, col_idx, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % player_count]

if __name__ == "__main__":
    main()
