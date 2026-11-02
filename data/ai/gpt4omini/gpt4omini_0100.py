import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # A, B, C, D, E, F, G
    print("+---" + "---+" * (COLS - 1) + "---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * (COLS - 1) + "---+")

def get_player_input(player):
    while True:
        column_label = input(f"Player {player}, please enter a column: ").upper()
        if len(column_label) == 1 and ord('A') <= ord(column_label) < ord('A') + COLS:
            return ord(column_label) - ord('A')  # Convert to index
        print("Invalid input. Please choose a valid column.")

def place_checker(board, column, checker):
    for row in reversed(board):  # Traverse from bottom to top
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        column = get_player_input(current_player)

        if place_checker(board, column, current_player):
            print_board(board)

            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break

            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full, try another column.")

if __name__ == "__main__":
    play_game()
