import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(64 + COLS):
            return ord(column) - 65
        print("Invalid input. Please try again.")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Check diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Check diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    turn_counter = 0

    print_board(board)

    while True:
        column = get_valid_input(current_player)
        if place_checker(board, column, current_player):
            turn_counter += 1
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if turn_counter >= ROWS * COLS:
                print("The game is a draw!")
                break

            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
