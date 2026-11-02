import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ["X", "O"]  # For 3 players use ["X", "O", "V"], etc.

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def is_valid_input(column, max_columns):
    return column.isalpha() and len(column) == 1 and 0 <= ord(column) - 65 < max_columns

def check_for_win(board, checker):
    # Check horizontal, vertical, and both diagonals
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][c] == checker for c in range(col, col + 4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[r][col] == checker for r in range(row, row + 4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    current_checker = PLAYERS[current_player_index]

    while True:
        clear_screen()
        print_board(board)
        column_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        if is_valid_input(column_input, COLUMNS):
            column_index = ord(column_input) - 65
            if place_checker(board, column_index, current_checker):
                if check_for_win(board, current_checker):
                    clear_screen()
                    print_board(board)
                    print(f"Player {current_checker} won!")
                    break
                if is_draw(board):
                    clear_screen()
                    print_board(board)
                    print("The game is a draw!")
                    break
                current_player_index = (current_player_index + 1) % len(PLAYERS)
                current_checker = PLAYERS[current_player_index]
            else:
                print("Column is full. Turn lost.")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
