import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with given dimensions and initialize with whitespaces."""
    return [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_number):
    """Return the checker for a given player number."""
    return CHECKERS[player_number]

def get_column_index(column):
    """Return the column index for a given column letter."""
    return ord(column) - ord('A')

def is_valid_input(column):
    """Check if the input is a valid column letter."""
    return column in string.ascii_uppercase[:BOARD_COLUMNS]

def is_column_full(board, column):
    """Check if a column is full."""
    return board[0][get_column_index(column)]!= " "

def get_next_available_row(board, column):
    """Get the next available row in a column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][get_column_index(column)] == " ":
            return row
    return None

def place_checker(board, player_checker, column):
    """Place a checker in a column."""
    row = get_next_available_row(board, column)
    if row is not None:
        board[row][get_column_index(column)] = player_checker
        return True
    return False

def check_win(board, player_checker):
    """Check for a win in all directions."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if all([board[row][col + i] == player_checker for i in range(4)]):
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS):
            if all([board[row + i][col] == player_checker for i in range(4)]):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if all([board[row + i][col + i] == player_checker for i in range(4)]):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if all([board[row - i][col + i] == player_checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    return all([all([cell!= " " for cell in row]) for row in board])

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board)
        print("Player {}, please enter a column:".format(get_player_checker(current_player)))

        column = input().upper()
        while not is_valid_input(column) or is_column_full(board, column):
            print("Invalid input. Please enter a valid column.")
            column = input().upper()

        if place_checker(board, get_player_checker(current_player), column):
            if check_win(board, get_player_checker(current_player)):
                os.system('clear')
                print_board(board)
                print("Player {} won!".format(get_player_checker(current_player)))
                break
            elif check_draw(board):
                os.system('clear')
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
