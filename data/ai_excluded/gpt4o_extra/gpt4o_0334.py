import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_CHECKERS = ["X", "O"]

def clear_screen():
    os.system('clear')  # Clears the screen for *nix systems

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join([chr(65 + col) for col in range(COLUMNS)]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_input(column_input):
    return len(column_input) == 1 and column_input.isalpha() and column_input.isupper()

def get_column_index(column_input):
    return ord(column_input) - 65

def drop_checker(board, column_index, player_checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = player_checker
            return True
    return False

def check_for_win(board, player_checker):
    # Check horizontally, vertically and diagonally
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True
    
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True
    
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board()
    player_count = len(PLAYER_CHECKERS)
    current_player = random.randint(0, player_count - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = PLAYER_CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")

        user_input = input().strip()
        if not is_valid_input(user_input):
            print("Invalid input. Please try again.")
            continue

        column_index = get_column_index(user_input)
        if column_index < 0 or column_index >= COLUMNS:
            print("Invalid column. Please try again.")
            continue

        if not drop_checker(board, column_index, current_checker):
            print("Column is full. You lose the turn.")
            current_player = (current_player + 1) % player_count
            continue

        if check_for_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_for_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % player_count

play_game()
