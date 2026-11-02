import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    col_labels = [chr(i + ord('A')) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))
    print("+---" * NUM_COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

def switch_player(current):
    return (current + 1) % NUM_PLAYERS

def is_valid_input(input_col):
    if len(input_col) != 1:
        return False
    return 'A' <= input_col <= chr(ord('A') + NUM_COLS - 1)

def get_column_number(input_col):
    return ord(input_col) - ord('A')

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True

    # Vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = PLAYER_CHECKERS[current_player]
        input_col = input(f"Player {player_checker}, please enter a column: ").strip().upper()

        while not is_valid_input(input_col):
            input_col = input(f"Invalid input! Player {player_checker}, please enter a valid column: ").strip().upper()

        col_number = get_column_number(input_col)

        if not place_checker(board, col_number, player_checker):
            print(f"Column {input_col} is full! You lose your turn.")
            current_player = switch_player(current_player)
            continue

        print_board(board)

        if check_for_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_for_draw(board):
            print("The game is a draw.")
            break

        current_player = switch_player(current_player)

if __name__ == "__main__":
    play_game()
