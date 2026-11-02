import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with the given dimensions"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def get_player_checker(player_index):
    """Get the checker symbol for the given player"""
    return CHECKERS[player_index % MAX_PLAYERS]

def is_valid_column(column):
    """Check if the given column is valid"""
    return "A" <= column <= "G"

def get_column_index(column):
    """Get the index of the given column"""
    return ord(column) - ord("A")

def is_column_full(board, column_index):
    """Check if the given column is full"""
    return board[0][column_index]!= " "

def place_checker(board, column_index, checker):
    """Place the checker in the given column"""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column_index] == " ":
            board[row_index][column_index] = checker
            return

def check_win(board, checker):
    """Check if the given checker has won"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
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
    # Set the number of players
    num_players = 2

    # Create the board
    board = create_board()

    # Choose a random player to start
    current_player = random.randint(0, num_players - 1)

    # Main game loop
    while True:
        # Clear the screen
        os.system('clear')

        # Print the current state of the board
        print_board(board)

        # Get the current player's checker
        checker = get_player_checker(current_player)

        # Get the column from the user
        while True:
            column = input(f"Player {checker}, please enter a column: ").upper()
            if is_valid_column(column):
                column_index = get_column_index(column)
                if not is_column_full(board, column_index):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid column, please enter a letter between A and G.")

        # Place the checker in the chosen column
        place_checker(board, column_index, checker)

        # Check if the current player has won
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
