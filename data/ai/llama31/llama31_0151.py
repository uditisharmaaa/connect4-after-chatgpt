import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized to whitespace"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board to the console"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_index):
    """Return the checker for the given player index"""
    return CHECKERS[player_index]

def get_column_index(column_letter):
    """Return the column index for the given column letter"""
    return ord(column_letter) - ord('A')

def is_valid_column(column_index):
    """Check if the column index is within the board boundaries"""
    return 0 <= column_index < BOARD_COLS

def is_valid_input(column_letter):
    """Check if the input column letter is valid"""
    return column_letter.isalpha() and len(column_letter) == 1 and is_valid_column(get_column_index(column_letter))

def get_next_open_row(board, column_index):
    """Return the next open row index for the given column index"""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column_index] == " ":
            return row_index
    return -1

def drop_checker(board, column_index, checker):
    """Drop the checker into the column"""
    row_index = get_next_open_row(board, column_index)
    if row_index!= -1:
        board[row_index][column_index] = checker
        return True
    return False

def check_win(board, checker):
    """Check if the given checker has won"""
    # Check horizontal locations for win
    for row_index in range(BOARD_ROWS):
        for column_index in range(BOARD_COLS - 3):
            if board[row_index][column_index] == checker and board[row_index][column_index + 1] == checker and board[row_index][column_index + 2] == checker and board[row_index][column_index + 3] == checker:
                return True

    # Check vertical locations for win
    for column_index in range(BOARD_COLS):
        for row_index in range(BOARD_ROWS - 3):
            if board[row_index][column_index] == checker and board[row_index + 1][column_index] == checker and board[row_index + 2][column_index] == checker and board[row_index + 3][column_index] == checker:
                return True

    # Check positively sloped diagonals
    for row_index in range(BOARD_ROWS - 3):
        for column_index in range(BOARD_COLS - 3):
            if board[row_index][column_index] == checker and board[row_index + 1][column_index + 1] == checker and board[row_index + 2][column_index + 2] == checker and board[row_index + 3][column_index + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row_index in range(3, BOARD_ROWS):
        for column_index in range(BOARD_COLS - 3):
            if board[row_index][column_index] == checker and board[row_index - 1][column_index + 1] == checker and board[row_index - 2][column_index + 2] == checker and board[row_index - 3][column_index + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board()

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        # Print the board
        print_board(board)

        # Get the current player's checker
        current_checker = get_player_checker(current_player_index)

        # Ask the player for input
        while True:
            column_letter = input("Player {}, please enter a column: ".format(current_checker))
            if is_valid_input(column_letter):
                column_index = get_column_index(column_letter)
                if drop_checker(board, column_index, current_checker):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input, please enter a column letter.")

        # Check if the current player has won
        if check_win(board, current_checker):
            print_board(board)
            print("Player {} won!".format(current_checker))
            break

        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
