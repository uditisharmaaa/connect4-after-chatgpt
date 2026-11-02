import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a 2D board with all elements initialized to whitespaces"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board with column labels"""
    print("  A B C D E F G")
    for row in board:
        print("+---+" * BOARD_COLS)
        print("| {} |".format(" | ".join(row)))
    print("+---+" * BOARD_COLS)

def is_valid_move(board, col):
    """Check if a move is valid (column not full)"""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Get the next open row in a column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def drop_checker(board, row, col, checker):
    """Drop a checker into the board at the specified row and column"""
    board[row][col] = checker

def check_win(board, checker):
    """Check for a win in all directions (horizontal, vertical, diagonal)"""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the board is full (draw)"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board(BOARD_ROWS, BOARD_COLS)

    # Set the number of players
    num_players = 2

    # Choose a random first player
    first_player = random.randint(0, num_players - 1)

    # Initialize the current player
    current_player = first_player

    # Game loop
    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Get the current player's checker
        current_checker = CHECKERS[current_player]

        # Ask the player for their move
        move = input("Player {}, please enter a column (A-{}): ".format(current_checker, chr(65 + BOARD_COLS - 1)))

        # Validate the move
        if not move.isalpha() or not move.upper().isalpha() or not 65 <= ord(move.upper()) <= 65 + BOARD_COLS - 1:
            print("Invalid input. Please enter a column letter.")
            continue

        # Get the column index from the move
        col = ord(move.upper()) - 65

        # Check if the move is valid
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue

        # Get the next open row in the column
        row = get_next_open_row(board, col)

        # Drop the checker into the board
        drop_checker(board, row, col, current_checker)

        # Check for a win
        if check_win(board, current_checker):
            print_board(board)
            print("Player {} won!".format(current_checker))
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
