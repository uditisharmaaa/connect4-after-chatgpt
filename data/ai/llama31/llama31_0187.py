import os
import random

# Constant global variables
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized to whitespaces"""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| " + " | ".join(row) + " |")
    print("+---+---+---+---+---+---+---+")

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return len(input_str) == 1 and "A" <= input_str.upper() <= chr(ord("A") + NUM_COLS - 1)

def get_player_checker(player_index):
    """Get the checker symbol for a player"""
    return CHECKERS[player_index]

def drop_checker(board, column, checker):
    """Drop a checker into a column"""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            break

def check_win(board, checker):
    """Check if a player has won"""
    # Check horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

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

    # Choose a random player to start
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        # Clear the screen
        os.system('clear')

        # Print the current state of the board
        print_board(board)

        # Get the current player's checker
        checker = get_player_checker(current_player)

        # Ask the current player for input
        while True:
            input_str = input(f"Player {checker}, please enter a column: ")
            if is_valid_input(input_str):
                column = ord(input_str.upper()) - ord("A")
                break
            print("Invalid input. Please enter a valid column letter.")

        # Drop the checker into the chosen column
        drop_checker(board, column, checker)

        # Check if the current player has won
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
