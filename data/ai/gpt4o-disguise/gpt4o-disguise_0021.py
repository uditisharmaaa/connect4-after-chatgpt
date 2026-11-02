import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = CHECKERS[player]
            return

def check_winner(board, player):
    checker = CHECKERS[player]
    for row in range(ROWS):
        for col in range(COLS):
            if (row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4))) or \
               (col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4))) or \
               (row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4))) or \
               (row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    num_players = min(PLAYERS, len(CHECKERS))
    current_player = random.randint(0, num_players - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        col_input = input().strip().upper()
        col = ord(col_input) - ord('A')
        if is_valid_move(board, col):
            make_move(board, col, current_player)
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % num_players
        else:
            print("Invalid move, please try again.")

main()
