import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Players' checkers

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + col) for col in range(COLUMNS)))
    print("+---" + ("+---" * (COLUMNS - 1)) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + ("+---" * (COLUMNS - 1)) + "+")

def is_valid_input(column_letter):
    return column_letter.isalpha() and len(column_letter) == 1 and 'A' <= column_letter <= 'A' + COLUMNS - 1

def find_lowest_empty_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, checker):
    row = find_lowest_empty_row(board, col)
    if row != -1:
        board[row][col] = checker
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
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, 1)  # Start with a random player (0 or 1)
    players_count = 2  # Set to 2 players
    current_player = PLAYERS[current_player_index]

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A to {chr(65 + COLUMNS - 1)}): ", end="")
        
        while True:
            column_input = input().strip().upper()
            if is_valid_input(column_input):
                column_index = ord(column_input) - 65
                if place_checker(board, column_index, current_player):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a valid column letter.")

        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_index = (current_player_index + 1) % players_count
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
