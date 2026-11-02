import os
import random

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Creates a 2D board with specified rows and columns."""
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen
    print("  A", end="")  # Print column labels
    for col in range(1, BOARD_COLS):
        print("   " + chr(ord('A') + col), end="")
    print()
    print("+" + "---+" * BOARD_COLS)
    for row in range(BOARD_ROWS):
        print("|", end="")  # Print row
        for col in range(BOARD_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+" + "---+" * BOARD_COLS)

def is_valid_input(input_str):
    """Checks if the input is a valid column letter."""
    return len(input_str) == 1 and 'A' <= input_str.upper() <= 'G'

def get_player_checker(player_num):
    """Returns the checker for the given player number."""
    return CHECKERS[player_num - 1]

def drop_checker(board, player_num, col):
    """Drops the checker into the specified column."""
    checker = get_player_checker(player_num)
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

def check_win(board, player_num):
    """Checks if the given player has won."""
    checker = get_player_checker(player_num)
    # Check horizontal wins
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and
                    board[row][col + 1] == checker and
                    board[row][col + 2] == checker and
                    board[row][col + 3] == checker):
                return True
    # Check vertical wins
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if (board[row][col] == checker and
                    board[row + 1][col] == checker and
                    board[row + 2][col] == checker and
                    board[row + 3][col] == checker):
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and
                    board[row + 1][col + 1] == checker and
                    board[row + 2][col + 2] == checker and
                    board[row + 3][col + 3] == checker):
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and
                    board[row - 1][col + 1] == checker and
                    board[row - 2][col + 2] == checker and
                    board[row - 3][col + 3] == checker):
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    # Set the number of players
    num_players = 2

    # Create the board
    board = create_board()

    # Choose a random player to start
    current_player = random.randint(1, num_players)

    while True:
        # Print the current state of the board
        print_board(board)

        # Get the current player's input
        while True:
            input_str = input("Player " + get_player_checker(current_player) +
                              ", please enter a column: ").upper()
            if is_valid_input(input_str):
                col = ord(input_str) - ord('A')
                if board[0][col]!= " ":
                    print("Column is full. Please choose another column.")
                else:
                    break
            else:
                print("Invalid input. Please enter a column letter.")

        # Drop the checker into the specified column
        drop_checker(board, current_player, col)

        # Check if the current player has won
        if check_win(board, current_player):
            print_board(board)
            print("Player " + get_player_checker(current_player) + " won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player % num_players) + 1

if __name__ == "__main__":
    main()
