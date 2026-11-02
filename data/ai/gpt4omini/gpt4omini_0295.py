import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # Expandable for more players if needed

def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column headers
    print("+" + "---+".join([''] * COLUMNS) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+".join([''] * COLUMNS) + "+")

def valid_input(column):
    if len(column) != 1 or column not in 'ABCDEFG':
        return False
    col_index = ord(column) - 65
    return 0 <= col_index < COLUMNS

def get_column_choice(current_player):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if valid_input(column):
            return ord(column) - 65
        print("Invalid input. Please choose a valid column (A-G).")

def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal (down-right and down-left)
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == checker:
                # Horizontal
                if col + 3 < COLUMNS and all(board[row][col + i] == checker for i in range(4)):
                    return True
                # Vertical
                if row + 3 < ROWS and all(board[row + i][col] == checker for i in range(4)):
                    return True
                # Diagonal (down-right)
                if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row + i][col + i] == checker for i in range(4)):
                    return True
                # Diagonal (down-left)
                if row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == checker for i in range(4)):
                    return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column = get_column_choice(current_player)

        if not place_checker(board, column, current_player):
            print("Column is full. Turn lost.")
            current_player_index = (current_player_index + 1) % len(PLAYERS)
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
