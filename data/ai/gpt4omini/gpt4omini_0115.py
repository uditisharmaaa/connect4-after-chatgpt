import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A to G
    print("+" + "---+" * COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print rows
        print("+" + "---+" * COLUMNS)  # Row separator

def is_valid_input(column):
    return column.isalpha() and 'A' <= column <= chr(65 + COLUMNS - 1)

def get_column_index(column):
    return ord(column) - 65

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_checker = PLAYERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        while True:
            user_input = input().upper()
            if is_valid_input(user_input):
                column_index = get_column_index(user_input)
                if place_checker(board, column_index, current_checker):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a valid column (A-G).")

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
