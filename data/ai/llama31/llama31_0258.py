import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = "XOVHM"

def create_board(rows, cols):
    """
    Create a 2D board with the specified number of rows and columns.
    Initialize all elements with whitespaces (" ").
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Print the current state of the board.
    """
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(string.ascii_uppercase[col], end="   ")
    print()
    # Print rows
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLUMNS + "+")

def get_player_checker(player_index):
    """
    Get the checker symbol for the specified player.
    """
    return CHECKERS[player_index]

def is_valid_input(col):
    """
    Check if the user input is a valid column label.
    """
    return col.upper() in string.ascii_uppercase[:COLUMNS]

def get_player_move(player_index, board):
    """
    Get the player's move (column label).
    Validate the input and ask for another input if it's invalid.
    """
    while True:
        col = input("Player {}, please enter a column: ".format(get_player_checker(player_index)))
        if is_valid_input(col):
            return string.ascii_uppercase.index(col.upper())
        print("Invalid input. Please enter a valid column label.")

def place_checker(board, player_index, col):
    """
    Place the player's checker in the specified column.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = get_player_checker(player_index)
            return

def check_win(board, player_index):
    """
    Check if the player has won the game.
    """
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == get_player_checker(player_index) and \
               board[row][col + 1] == get_player_checker(player_index) and \
               board[row][col + 2] == get_player_checker(player_index) and \
               board[row][col + 3] == get_player_checker(player_index):
                return True
    # Check vertical wins
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == get_player_checker(player_index) and \
               board[row + 1][col] == get_player_checker(player_index) and \
               board[row + 2][col] == get_player_checker(player_index) and \
               board[row + 3][col] == get_player_checker(player_index):
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == get_player_checker(player_index) and \
               board[row + 1][col + 1] == get_player_checker(player_index) and \
               board[row + 2][col + 2] == get_player_checker(player_index) and \
               board[row + 3][col + 3] == get_player_checker(player_index):
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == get_player_checker(player_index) and \
               board[row - 1][col + 1] == get_player_checker(player_index) and \
               board[row - 2][col + 2] == get_player_checker(player_index) and \
               board[row - 3][col + 3] == get_player_checker(player_index):
                return True
    return False

def check_draw(board):
    """
    Check if the game is a draw (i.e., the board is full).
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    # Create the board
    board = create_board(ROWS, COLUMNS)
    # Randomly select the first player
    current_player = random.randint(0, PLAYERS - 1)
    # Game loop
    while True:
        os.system('clear')
        print_board(board)
        # Get the player's move
        col = get_player_move(current_player, board)
        # Place the checker
        place_checker(board, current_player, col)
        # Check for a win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(get_player_checker(current_player)))
            break
        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
