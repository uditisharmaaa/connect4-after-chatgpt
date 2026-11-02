import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Rows
        print("+" + "---+" * COLS)  # Row separator

def is_valid_input(col_input):
    return col_input.isalpha() and col_input.upper() >= 'A' and col_input.upper() < chr(65 + COLS)

def get_column_index(col_input):
    return ord(col_input.upper()) - 65

def is_column_full(board, col_index):
    return board[0][col_index] != ' '

def get_next_open_row(board, col_index):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None

def place_checker(board, row, col_index, checker):
    board[row][col_index] = checker

def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    turn = random.randint(0, 1)  # Randomly selecting the first player
    game_over = False

    while not game_over:
        print_board(board)
        current_checker = PLAYERS[turn % len(PLAYERS)]
        col_input = input(f"Player {current_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ")

        while not is_valid_input(col_input) or is_column_full(board, get_column_index(col_input)):
            if not is_valid_input(col_input):
                print("Invalid input. Please enter a valid column letter.")
            else:
                print("Column is full. Choose a different column.")
            col_input = input(f"Player {current_checker}, please enter a column (A-{chr(65 + COLS - 1)}): ")

        col_index = get_column_index(col_input)
        row_index = get_next_open_row(board, col_index)
        place_checker(board, row_index, col_index, current_checker)

        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            turn += 1

if __name__ == "__main__":
    main()
