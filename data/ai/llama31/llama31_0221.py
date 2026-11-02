import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, player_turn):
    """Print the board with column labels"""
    print("  A B C D E F G")
    for row in board:
        print("+---" * BOARD_COLS)
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS)
    print(f"Player {CHECKERS[player_turn]}, please enter a column: ")

def is_valid_input(input_str, board):
    """Check if user input is valid"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    col_idx = ord(input_str.upper()) - ord('A')
    if col_idx < 0 or col_idx >= BOARD_COLS or board[0][col_idx]!= " ":
        return False
    return True

def drop_checker(board, col_idx, player_checker):
    """Drop a checker into a column"""
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_checker
            return

def check_win(board, player_checker):
    """Check for a win in all directions"""
    # Check horizontal
    for row in board:
        for col_idx in range(BOARD_COLS - 3):
            if row[col_idx] == player_checker and row[col_idx + 1] == player_checker and row[col_idx + 2] == player_checker and row[col_idx + 3] == player_checker:
                return True

    # Check vertical
    for col_idx in range(BOARD_COLS):
        for row_idx in range(BOARD_ROWS - 3):
            if board[row_idx][col_idx] == player_checker and board[row_idx + 1][col_idx] == player_checker and board[row_idx + 2][col_idx] == player_checker and board[row_idx + 3][col_idx] == player_checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player_checker and board[row_idx + 1][col_idx + 1] == player_checker and board[row_idx + 2][col_idx + 2] == player_checker and board[row_idx + 3][col_idx + 3] == player_checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row_idx in range(3, BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if board[row_idx][col_idx] == player_checker and board[row_idx - 1][col_idx + 1] == player_checker and board[row_idx - 2][col_idx + 2] == player_checker and board[row_idx - 3][col_idx + 3] == player_checker:
                return True

    return False

def is_draw(board):
    """Check if the board is full"""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Set number of players and board dimensions
    num_players = 2

    # Create board and print initial state
    board = create_board()
    os.system('clear')
    print_board(board, random.randint(0, num_players - 1))

    # Game loop
    current_player = 0
    while True:
        # Get user input
        input_str = input().upper()

        # Check if input is valid
        if not is_valid_input(input_str, board):
            os.system('clear')
            print_board(board, current_player)
            print("Invalid input. Please try again.")
            continue

        # Drop checker
        col_idx = ord(input_str) - ord('A')
        drop_checker(board, col_idx, CHECKERS[current_player])

        # Check for win
        if check_win(board, CHECKERS[current_player]):
            os.system('clear')
            print_board(board, current_player)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            os.system('clear')
            print_board(board, current_player)
            print("It's a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % num_players
        os.system('clear')
        print_board(board, current_player)

if __name__ == "__main__":
    main()
