import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create an empty Connect 4 board."""
    return [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_checker(player):
    """Get the checker for the given player."""
    return CHECKERS[player - 1]

def is_valid_move(board, column):
    """Check if the move is valid."""
    return board[0][column] == " "

def get_next_open_row(board, column):
    """Get the next open row in the given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            return row

def make_move(board, player, column):
    """Make a move on the board."""
    row = get_next_open_row(board, column)
    board[row][column] = get_checker(player)

def winning_move(board, player):
    """Check if the given player has won."""
    checker = get_checker(player)
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def is_board_full(board):
    """Check if the board is full."""
    for col in range(BOARD_COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board()
    player = random.randint(1, NUM_PLAYERS)
    print_board(board)
    while True:
        print("Player {}, please enter a column:".format(get_checker(player)))
        move = input().strip().upper()
        if move not in "ABCDEFG":
            print("Invalid input. Please try again.")
            continue
        column = ord(move) - 65
        if not is_valid_move(board, column):
            print("Column is full. Please try again.")
            continue
        make_move(board, player, column)
        print_board(board)
        if winning_move(board, player):
            print("Player {} won!".format(get_checker(player)))
            break
        if is_board_full(board):
            print("It's a draw!")
            break
        player = (player % NUM_PLAYERS) + 1

if __name__ == "__main__":
    main()
