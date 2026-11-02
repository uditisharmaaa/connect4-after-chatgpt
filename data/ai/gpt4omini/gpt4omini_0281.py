import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" + "---+" * COLS)  
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLS)

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col.upper() <= chr(65 + COLS - 1)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[ord(col) - 65] == " ":
            row[ord(col) - 65] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)

    while not game_over:
        print(f"Player {current_player}, please enter a column:")
        col = input().upper()

        while not is_valid_input(col) or not drop_checker(board, col, current_player):
            print("Invalid input. Please try again:")
            col = input().upper()

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
