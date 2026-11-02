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
    print("+---" + "+---" * (COLS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLS - 1) + "+")

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col) - 65

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[get_column_index(col)] == " ":
            row[get_column_index(col)] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == checker:
                if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        checker = PLAYERS[current_player_index]
        print(f"Player {checker}, please enter a column:")
        
        while True:
            col = input().upper()
            if is_valid_input(col) and place_checker(board, col, checker):
                break
            print("Invalid input, please try again.")

        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
