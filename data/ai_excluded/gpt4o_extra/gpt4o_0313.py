import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # You can change this to 3, 4, or 5 for more players
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

# Initialize the board
board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Randomly select the starting player
current_player = random.randint(0, PLAYERS - 1)

def print_board():
    os.system('clear')  # Clear the screen on Unix/Linux systems
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    return column.isalpha() and 0 <= ord(column) - 65 < COLUMNS

def is_column_full(column_index):
    return board[0][column_index] != " "

def place_checker(column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

def check_for_win(checker):
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal win (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal win (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_for_draw():
    return all(all(cell != " " for cell in row) for row in board)

def main():
    global current_player
    print_board()
    
    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column (A-{chr(65 + COLUMNS - 1)}):")
        column = input().strip().upper()

        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column_index = ord(column) - 65

        if is_column_full(column_index):
            print("Column is full. You lose your turn.")
        else:
            place_checker(column_index, current_checker)
            print_board()

            if check_for_win(current_checker):
                print(f"Player {current_checker} won!")
                break

            if check_for_draw():
                print("The game is a draw.")
                break

            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
