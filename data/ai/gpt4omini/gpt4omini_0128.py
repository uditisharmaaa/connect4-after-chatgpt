import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_column_index(col):
    return ord(col.upper()) - 65

def is_valid_input(col):
    return col.upper() in [chr(65 + i) for i in range(COLS)]

def place_checker(board, col, checker):
    col_idx = get_column_index(col)
    for row in reversed(board):  # Start checking from the bottom row
        if row[col_idx] == ' ':
            row[col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.randint(0, len(PLAYER_CHECKERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        checker = PLAYER_CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        while True:
            user_input = input().strip().upper()
            if is_valid_input(user_input):
                if place_checker(board, user_input, checker):
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a valid column letter (A-G).")

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True

        current_player = (current_player + 1) % len(PLAYER_CHECKERS)

if __name__ == "__main__":
    play_game()
