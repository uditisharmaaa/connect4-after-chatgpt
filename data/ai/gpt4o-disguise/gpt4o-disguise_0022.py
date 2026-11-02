import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_SIGNS = CHECKERS[:PLAYERS]

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_input(player_input):
    return player_input.isalpha() and len(player_input) == 1 and 'A' <= player_input <= chr(ord('A') + COLS - 1)

def place_checker(board, col, sign):
    col_idx = ord(col) - ord('A')
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = sign
            return True
    return False

def check_win(board, sign):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == sign for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == sign for i in range(4)):
                return True

    # Check diagonal /
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == sign for i in range(4)):
                return True

    # Check diagonal \
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == sign for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print(f"Player {PLAYER_SIGNS[current_player]}, please enter a column:")
        player_input = input().strip()

        if not is_valid_input(player_input):
            continue

        if not place_checker(board, player_input, PLAYER_SIGNS[current_player]):
            continue

        print_board(board)

        if check_win(board, PLAYER_SIGNS[current_player]):
            print(f"Player {PLAYER_SIGNS[current_player]} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
