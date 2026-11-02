import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """
    Create a 2D list representing the game board.
    All elements are initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Print the game board.
    """
    print("  A", end=" ")
    for col in range(1, BOARD_COLS):
        print(chr(ord("A") + col), end=" ")
    print()
    for row in range(BOARD_ROWS + 1):
        print("+---" * BOARD_COLS + "+")
        if row < BOARD_ROWS:
            print("|", end=" ")
            for col in range(BOARD_COLS):
                print(board[row][col], end=" | ")
            print()

def is_valid_input(input_str, board):
    """
    Check if the input is valid.
    A valid input is an uppercase letter corresponding to a column.
    """
    if not input_str.isalpha() or len(input_str)!= 1:
        return False
    col_idx = ord(input_str) - ord("A")
    if col_idx < 0 or col_idx >= BOARD_COLS:
        return False
    if board[0][col_idx]!= " ":
        return False
    return True

def place_checker(board, player, col_idx):
    """
    Place a checker in the specified column.
    The checker falls straight down, occupying the lowest available space.
    """
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = CHECKERS[player]
            return

def check_win(board, player):
    """
    Check if the current player has won.
    A player wins if 4 checkers in a row are placed on the board
    either horizontally, vertically or diagonally.
    """
    checker = CHECKERS[player]
    # Check horizontal
    for row_idx in range(BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if (board[row_idx][col_idx] == checker and
                    board[row_idx][col_idx + 1] == checker and
                    board[row_idx][col_idx + 2] == checker and
                    board[row_idx][col_idx + 3] == checker):
                return True
    # Check vertical
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS):
            if (board[row_idx][col_idx] == checker and
                    board[row_idx + 1][col_idx] == checker and
                    board[row_idx + 2][col_idx] == checker and
                    board[row_idx + 3][col_idx] == checker):
                return True
    # Check diagonal (top-left to bottom-right)
    for row_idx in range(BOARD_ROWS - 3):
        for col_idx in range(BOARD_COLS - 3):
            if (board[row_idx][col_idx] == checker and
                    board[row_idx + 1][col_idx + 1] == checker and
                    board[row_idx + 2][col_idx + 2] == checker and
                    board[row_idx + 3][col_idx + 3] == checker):
                return True
    # Check diagonal (bottom-left to top-right)
    for row_idx in range(3, BOARD_ROWS):
        for col_idx in range(BOARD_COLS - 3):
            if (board[row_idx][col_idx] == checker and
                    board[row_idx - 1][col_idx + 1] == checker and
                    board[row_idx - 2][col_idx + 2] == checker and
                    board[row_idx - 3][col_idx + 3] == checker):
                return True
    return False

def check_draw(board):
    """
    Check if the game is a draw.
    The game is a draw if the board is full and no player has won.
    """
    return all(cell!= " " for row in board for cell in row)

def main():
    # Set the number of players
    num_players = 2
    # Create the game board
    board = create_board(BOARD_ROWS, BOARD_COLS)
    # Choose a random player to start
    current_player = random.randint(0, num_players - 1)
    # Clear the screen and print the initial board
    os.system("clear")
    print_board(board)
    while True:
        # Get the current player's input
        input_str = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        # Validate the input
        if not is_valid_input(input_str, board):
            print("Invalid input. Please try again.")
            continue
        # Place the checker
        col_idx = ord(input_str) - ord("A")
        place_checker(board, current_player, col_idx)
        # Check if the current player has won
        if check_win(board, current_player):
            os.system("clear")
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        # Check if the game is a draw
        if check_draw(board):
            os.system("clear")
            print_board(board)
            print("It's a draw!")
            break
        # Switch to the next player
        current_player = (current_player + 1) % num_players
        # Clear the screen and print the updated board
        os.system("clear")
        print_board(board)

if __name__ == "__main__":
    main()
