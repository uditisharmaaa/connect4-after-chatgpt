import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col):
    return col.isalpha() and len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col) - 65

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_checker = PLAYERS[current_player_index]
        col = input(f"Player {current_checker}, please enter a column: ").upper()

        while not is_valid_input(col):
            col = input("Invalid input. Please enter a valid column: ").upper()

        column_index = get_column_index(col)

        if drop_checker(board, column_index, current_checker):
            print_board(board)

            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print(f"Column {col} is full! Try another column.")

if __name__ == "__main__":
    main()
