import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # Clear the terminal screen (Linux/Unix)

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def initialize_board():
    return [[" "]*COLUMNS for _ in range(ROWS)]

def get_first_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_column(column_choice, board):
    if column_choice.isalpha() and len(column_choice) == 1:
        col_idx = ord(column_choice.upper()) - 65
        if 0 <= col_idx < COLUMNS and board[0][col_idx] == " ":
            return True
    return False

def place_checker(board, col_idx, checker):
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return

def check_for_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col+i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row+i][col-i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game(num_players, board):
    current_player = get_first_player(num_players)
    while True:
        print_board(board)
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column:")
        column_choice = input().strip()
        
        if not is_valid_column(column_choice, board):
            print("Invalid input, try again.")
            continue
        
        col_idx = ord(column_choice.upper()) - 65
        place_checker(board, col_idx, checker)

        if check_for_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

def main():
    board = initialize_board()
    num_players = 2  # Change this value to add more players (up to 5)
    play_game(num_players, board)

if __name__ == "__main__":
    main()
