import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # Add more symbols for more players if needed

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(ord('A') + c) for c in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def drop_checker(board, column, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return True
    return False

def is_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)

    print_board(board)

    while True:
        valid_input = False
        while not valid_input:
            column_input = input(f"Player {current_player}, please enter a column (A-{chr(ord('A') + COLUMNS - 1)}): ").strip().upper()
            if len(column_input) == 1 and 'A' <= column_input <= chr(ord('A') + COLUMNS - 1):
                column = ord(column_input) - ord('A')
                if drop_checker(board, column, current_player):
                    valid_input = True
                else:
                    print("Column is full. Please choose a different column.")
            else:
                print("Invalid input. Please enter a valid column letter.")

        print_board(board)

        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
