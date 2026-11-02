import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WINNING_COUNT = 4

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))  # Column headers
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def validate_input(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < COLS and board[0][col_index] == " "

def place_checker(board, column, checker):
    col_index = ord(column.upper()) - 65
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                if (check_direction(board, row, col, 0, 1, checker) or  # Horizontal
                    check_direction(board, row, col, 1, 0, checker) or  # Vertical
                    check_direction(board, row, col, 1, 1, checker) or  # Diagonal \
                    check_direction(board, row, col, 1, -1, checker)):  # Diagonal /
                    return True
    return False

def check_direction(board, row, col, d_row, d_col, checker):
    count = 0
    for _ in range(WINNING_COUNT):
        if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
            count += 1
            if count == WINNING_COUNT:
                return True
        row += d_row
        col += d_col
    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS[:2])
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()

        if not validate_input(user_input, board):
            print("Invalid input. Please try again.")
            continue
        
        place_checker(board, user_input, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw.")
            break

        # Switch to the next player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % 2]

if __name__ == "__main__":
    main()
