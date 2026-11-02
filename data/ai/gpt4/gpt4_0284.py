import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    width = len(board[0])
    print("  " + "   ".join(chr(ord('A') + c) for c in range(width)))
    print("+---" * width + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * width + "+")

def validate_column(input_column, board):
    if len(input_column) != 1 or not input_column.isalpha():
        return False
    column_index = ord(input_column.upper()) - ord('A')
    if column_index < 0 or column_index >= len(board[0]):
        return False
    if board[0][column_index] != EMPTY_CELL:
        return False
    return True

def get_column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == EMPTY_CELL:
            row[column_index] = checker
            return

def is_winning_move(board, player_checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == player_checker:
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == player_checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == player_checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == player_checker:
                return True

    return False

def is_draw(board):
    return all(board[0][c] != EMPTY_CELL for c in range(len(board[0])))

def main():
    # Initialize the game
    board = initialize_board(ROWS, COLUMNS)
    player_count = PLAYERS
    checkers = CHECKERS[:player_count]
    player_turn = random.randint(0, player_count - 1)

    clear_screen()
    print_board(board)

    while True:
        current_checker = checkers[player_turn]
        print(f"Player {current_checker}, please enter a column:")
        column_input = input().strip()

        while not validate_column(column_input, board):
            print("Invalid input. Please enter a valid column:")
            column_input = input().strip()

        column_index = get_column_index(column_input)
        place_checker(board, column_index, current_checker)

        clear_screen()
        print_board(board)

        # Check for win or draw
        if is_winning_move(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch turns
        player_turn = (player_turn + 1) % player_count

if __name__ == "__main__":
    main()
