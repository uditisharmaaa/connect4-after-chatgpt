import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))  # Column labels A, B, C....
    print("+---" * COLUMNS + "+") 
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def valid_input(column_choice, board):
    if len(column_choice) != 1 or column_choice not in [chr(i) for i in range(65, 65 + COLUMNS)]:
        return False
    column_index = ord(column_choice) - 65
    if board[0][column_index] != " ":
        return False
    return True

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                # Check horizontal
                if c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Check diagonal /
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    num_players = 2
    players = PLAYERS[:num_players]
    current_player = random.choice(players)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column_choice = input().upper()

        while not valid_input(column_choice, board):
            print("Invalid input, please try again:")
            column_choice = input().upper()

        column_index = ord(column_choice) - 65
        place_checker(board, column_index, current_player)

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
