import random
import os

COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYERS_CHECKERS = CHECKERS[:PLAYERS]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65+i) for i in range(COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_col_input():
    while True:
        try:
            col = input("Please enter a column: ").upper()
            if len(col) == 1 and 'A' <= col <= chr(65+COLS-1):
                return ord(col) - 65
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_for_win(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != checker:
                continue
            if col + 3 < COLS and all(board[row][col+i] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and all(board[row+i][col] == checker for i in range(4)):
                return True
            if row + 3 < ROWS and col + 3 < COLS and all(board[row+i][col+i] == checker for i in range(4)):
                return True
            if row - 3 >= 0 and col + 3 < COLS and all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = PLAYERS_CHECKERS[current_player_index]
        print(f"Player {current_checker}'s turn.")
        col = get_col_input()

        if place_checker(board, col, current_checker):
            print_board(board)
            if check_for_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            elif check_for_draw(board):
                print("It's a draw!")
                break
            current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print("Column is full. Try another one.")

if __name__ == "__main__":
    play_game()
