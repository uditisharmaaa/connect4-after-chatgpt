import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Create a 2D board with all elements initialized with whitespaces.
    """
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """
    Print the current state of the board.
    """
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+" * BOARD_COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---+" * BOARD_COLS)

def get_checker(player):
    """
    Return the checker for the given player.
    """
    return CHECKERS[player - 1]

def is_valid_input(input_str):
    """
    Check if the input is a valid column letter.
    """
    return len(input_str) == 1 and "A" <= input_str.upper() <= chr(64 + BOARD_COLS)

def get_column(input_str):
    """
    Convert the input column letter to a 0-based index.
    """
    return ord(input_str.upper()) - 65

def is_column_full(board, column):
    """
    Check if the given column is full.
    """
    return board[0][column]!= " "

def place_checker(board, column, checker):
    """
    Place the checker in the given column.
    """
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win(board, checker):
    """
    Check for a win in the given board.
    """
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """
    Check if the game is a draw.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board()

    # Choose a random player to start
    current_player = random.randint(1, PLAYERS)

    while True:
        # Clear the screen and print the board
        os.system('clear')
        print_board(board)

        # Get the current player's checker
        checker = get_checker(current_player)

        # Ask the player for input
        while True:
            input_str = input(f"Player {checker}, please enter a column: ")
            if is_valid_input(input_str):
                column = get_column(input_str)
                if not is_column_full(board, column):
                    break
                else:
                    print("Column is full, please choose another one.")
            else:
                print("Invalid input, please enter a column letter.")

        # Place the checker
        place_checker(board, column, checker)

        # Check for a win
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player % PLAYERS) + 1

if __name__ == "__main__":
    main()
