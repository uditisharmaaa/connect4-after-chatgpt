import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))  # Column headers A-G
    print("+---" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row data
        print("+---" + "---+" * COLS)  # Borders between rows

def drop_checker(board, column, checker):
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def is_winner(board, checker):
    # Check horizontally, vertically and diagonally
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def is_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS[:2])  # Choose randomly between the first two players

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ")
        column_input = input().strip().upper()

        if len(column_input) != 1 or not ('A' <= column_input <= chr(65 + COLS - 1)):
            print("Invalid input. Please try again.")
            continue

        column = ord(column_input) - 65  # Convert letter to column index

        if not drop_checker(board, column, current_player):
            print("Column is full. Please try again.")
            continue

        print_board(board)

        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_full(board):
            print("The game is a draw.")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
