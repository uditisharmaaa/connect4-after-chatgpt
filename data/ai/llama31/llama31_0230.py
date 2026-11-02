import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Player checkers
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Create a 2D board with the specified width and height.
    All elements are initialized with whitespaces.
    """
    return [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """
    Print the board with column labels and rows.
    """
    print("  " + " ".join(string.ascii_uppercase[:BOARD_WIDTH]))
    for row in board:
        print("+---" * BOARD_WIDTH + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_WIDTH + "+")

def validate_input(column):
    """
    Validate the user input.
    Check if the input is a single uppercase letter within the board width.
    """
    if len(column)!= 1 or not column.isalpha() or not column.isupper():
        return False
    return string.ascii_uppercase.index(column) < BOARD_WIDTH

def get_player_move(player_name):
    """
    Ask the player for a column and validate the input.
    """
    while True:
        column = input(f"Player {player_name}, please enter a column: ")
        if validate_input(column):
            return column
        print("Invalid input. Please enter a single uppercase letter.")

def place_checker(board, column, checker):
    """
    Place the checker in the specified column.
    Find the lowest available space within the column.
    """
    column_index = string.ascii_uppercase.index(column)
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_win(board):
    """
    Check for a win (horizontally, vertically, or diagonally).
    """
    # Horizontal
    for row in board:
        for i in range(BOARD_WIDTH - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3]!= " ":
                return row[i]
    # Vertical
    for col in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col]!= " ":
                return board[i][col]
    # Diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]!= " ":
                return board[row][col]
    # Diagonal (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]!= " ":
                return board[row][col]
    return None

def check_draw(board):
    """
    Check if the board is full (draw).
    """
    return all(cell!= " " for row in board for cell in row)

def game():
    # Create the board
    board = create_board()

    # Set the number of players
    num_players = 2

    # Choose a random first player
    players = PLAYER_CHECKERS[:num_players]
    first_player = random.choice(players)
    players.remove(first_player)
    players.insert(0, first_player)

    # Clear the screen and print the board
    os.system('clear')
    print_board(board)

    # Game loop
    while True:
        for player in players:
            # Ask the player for a column
            column = get_player_move(player)

            # Place the checker
            place_checker(board, column, player)

            # Clear the screen and print the updated board
            os.system('clear')
            print_board(board)

            # Check for a win
            winner = check_win(board)
            if winner:
                print(f"Player {winner} won!")
                return

            # Check for a draw
            if check_draw(board):
                print("It's a draw!")
                return

if __name__ == "__main__":
    game()
