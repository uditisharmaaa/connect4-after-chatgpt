import os
import random
import string

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Mapping of player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Create an empty board with the specified dimensions.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Print the current state of the board.
    """
    print("  " + " ".join(string.ascii_uppercase[:COLUMNS]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_player_checker(player_index):
    """
    Get the checker symbol for the specified player.
    """
    return PLAYER_CHECKERS[player_index % len(PLAYER_CHECKERS)]

def get_valid_input(player_name):
    """
    Get a valid column input from the player.
    """
    while True:
        column = input(f"{player_name}, please enter a column: ")
        if column in string.ascii_uppercase[:COLUMNS]:
            return column
        print("Invalid input. Please enter a letter from A to G.")

def drop_checker(board, column, checker):
    """
    Drop the checker into the specified column.
    """
    for row in reversed(board):
        if row[string.ascii_uppercase.index(column)] == " ":
            row[string.ascii_uppercase.index(column)] = checker
            return

def check_win(board, checker):
    """
    Check if the specified player has won.
    """
    # Check horizontal locations for win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """
    Check if the game is a draw.
    """
    return all(all(cell!= " " for cell in row) for row in board)

def main():
    # Set the number of players
    num_players = 2

    # Create the board
    board = create_board()

    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        # Clear the screen
        os.system('clear')

        # Print the current state of the board
        print_board(board)

        # Get the current player's name and checker
        player_name = f"Player {get_player_checker(current_player)}"
        player_checker = get_player_checker(current_player)

        # Get a valid column input from the player
        column = get_valid_input(player_name)

        # Drop the checker into the specified column
        drop_checker(board, column, player_checker)

        # Check if the current player has won
        if check_win(board, player_checker):
            print_board(board)
            print(f"{player_name} won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
