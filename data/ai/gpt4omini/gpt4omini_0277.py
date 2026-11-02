import os
import random

ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
current_player = random.choice(PLAYERS[:2])

def print_board():
    os.system('clear')
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def is_valid_column(col):
    return 0 <= col < COLS and board[0][col] == " "

def place_checker(col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = current_player
            return True
    return False

def check_winner():
    # Horizontal, vertical, and diagonal checks
    for row in range(ROWS):
        for col in range(COLS-3):
            if board[row][col] == current_player and board[row][col+1] == current_player and board[row][col+2] == current_player and board[row][col+3] == current_player:
                return True

    for col in range(COLS):
        for row in range(ROWS-3):
            if board[row][col] == current_player and board[row+1][col] == current_player and board[row+2][col] == current_player and board[row+3][col] == current_player:
                return True

    for row in range(ROWS-3):
        for col in range(COLS-3):
            if board[row][col] == current_player and board[row+1][col+1] == current_player and board[row+2][col+2] == current_player and board[row+3][col+3] == current_player:
                return True

    for row in range(3, ROWS):
        for col in range(COLS-3):
            if board[row][col] == current_player and board[row-1][col+1] == current_player and board[row-2][col+2] == current_player and board[row-3][col+3] == current_player:
                return True

    return False

def is_draw():
    return all(board[0][col] != " " for col in range(COLS))

def main():
    global current_player
    print_board()
    for turn in range(ROWS * COLS):
        while True:
            try:
                col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
                if len(col_input) != 1 or col_input < 'A' or col_input > chr(65 + COLS - 1):
                    raise ValueError("Invalid column")
                col = ord(col_input) - 65
                if is_valid_column(col):
                    place_checker(col)
                    break
                else:
                    print("Column is full, choose another column.")
            except ValueError:
                print("Please enter a valid column letter (A-G).")

        print_board()
        if check_winner():
            print(f"Player {current_player} won!")
            return
        if is_draw():
            print("The game is a draw!")
            return
        current_player = PLAYERS[PLAYERS.index(current_player) + 1 % len(PLAYERS)]

if __name__ == "__main__":
    main()
