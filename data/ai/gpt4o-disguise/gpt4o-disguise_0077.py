import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
BOARD = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + "   ".join([chr(i) for i in range(ord('A'), ord('A') + COLS)]))
    for row in BOARD:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_column_index(column):
    if len(column) == 1 and 'A' <= column <= chr(ord('A') + COLS - 1):
        return ord(column) - ord('A')
    return -1

def place_checker(player, column):
    for row in reversed(BOARD):
        if row[column] == ' ':
            row[column] = CHECKERS[player]
            return True
    return False

def check_winner():
    for r in range(ROWS):
        for c in range(COLS):
            if BOARD[r][c] != ' ':
                if check_direction(r, c, 1, 0) or check_direction(r, c, 0, 1) or check_direction(r, c, 1, 1) or check_direction(r, c, 1, -1):
                    return True
    return False

def check_direction(r, c, dr, dc):
    consecutive = 0
    for i in range(4):
        nr, nc = r + i * dr, c + i * dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and BOARD[nr][nc] == BOARD[r][c]:
            consecutive += 1
        else:
            break
    return consecutive == 4

def check_draw():
    return all(BOARD[0][c] != ' ' for c in range(COLS))

def main():
    player = random.randint(0, NUM_PLAYERS - 1)
    while True:
        print_board()
        print("Player", CHECKERS[player], "please enter a column:")
        column_input = input().strip().upper()
        column = get_column_index(column_input)
        if column >= 0:
            if place_checker(player, column):
                if check_winner():
                    print_board()
                    print("Player", CHECKERS[player], "won!")
                    break
                if check_draw():
                    print_board()
                    print("It's a draw!")
                    break
                player = (player + 1) % NUM_PLAYERS
            else:
                print("Column full. Turn lost.")
        else:
            print("Invalid input. Please enter a valid column.")

main()
