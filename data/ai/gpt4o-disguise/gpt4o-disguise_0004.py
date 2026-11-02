import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def init_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "  ".join([chr(i + 65) for i in range(len(board[0]))]))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def check_win(board, player):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[row][col] != " " for row in range(ROWS) for col in range(COLS))

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def main():
    board = init_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        player_checker = CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        while True:
            column_input = input().strip().upper()
            if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLS - 1):
                col = ord(column_input) - 65
                if drop_checker(board, col, player_checker):
                    break
                else:
                    print(f"Column {column_input} is full. Choose another column.")
            else:
                print("Invalid input. Choose a valid column.")

        print_board(board)

        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
