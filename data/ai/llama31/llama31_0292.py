import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a new 2D board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end="   ")
        for cell in row:
            print(cell, end="   ")
        print("|")
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_id):
    """Get the checker for the given player."""
    return PLAYERS[player_id % len(PLAYERS)]

def is_valid_input(input_str, cols):
    """Check if the input is a valid column letter."""
    return len(input_str) == 1 and "A" <= input_str.upper() <= chr(ord("A") + cols - 1)

def get_col_from_input(input_str, cols):
    """Get the column index from the input string."""
    return ord(input_str.upper()) - ord("A")

def is_column_full(board, col):
    """Check if the given column is full."""
    return board[0][col]!= " "

def place_checker(board, player_id, col):
    """Place the checker of the given player in the given column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = get_player_checker(player_id)
            return

def check_win(board, player_id):
    """Check if the given player has won."""
    checker = get_player_checker(player_id)
    # Check horizontal locations for win
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    # Check vertical locations for win
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check positively sloped diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check negatively sloped diagonals
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    num_players = 2
    board = create_board(BOARD_ROWS, BOARD_COLS)
    player_id = random.randint(0, num_players - 1)
    while True:
        os.system('clear')
        print_board(board)
        input_str = input("Player " + get_player_checker(player_id) + ", please enter a column: ")
        if not is_valid_input(input_str, BOARD_COLS):
            print("Invalid input. Please try again.")
            continue
        col = get_col_from_input(input_str, BOARD_COLS)
        if is_column_full(board, col):
            print("Column is full. Please try again.")
            continue
        place_checker(board, player_id, col)
        if check_win(board, player_id):
            os.system('clear')
            print_board(board)
            print("Player " + get_player_checker(player_id) + " won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        player_id = (player_id + 1) % num_players

if __name__ == "__main__":
    main()
