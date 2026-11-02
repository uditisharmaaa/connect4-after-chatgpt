import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print("+---" * COLUMNS + "+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---" * COLUMNS + "+")

def get_player_checker(player):
    """Get the checker symbol for the given player."""
    return CHECKERS[player - 1]

def is_valid_input(column):
    """Check if the input is a valid column letter."""
    return column.isalpha() and column.upper() in "ABCDEFG"

def get_column_index(column):
    """Get the column index from the input letter."""
    return ord(column.upper()) - ord("A")

def is_column_full(board, column):
    """Check if the given column is full."""
    return board[0][column]!= " "

def drop_checker(board, column, checker):
    """Drop the checker in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            break

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if all(board[row][col] == checker for row in range(i, i+4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(all(cell!= " " for cell in row) for row in board)

def main():
    board = create_board()
    players = list(range(1, PLAYERS + 1))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        player = players[current_player]
        checker = get_player_checker(player)
        column = input(f"Player {player}, please enter a column: ")
        if not is_valid_input(column):
            print("Invalid input. Please enter a column letter.")
            continue
        column = get_column_index(column)
        if is_column_full(board, column):
            print("Column is full. Please choose another column.")
            continue
        drop_checker(board, column, checker)
        if check_win(board, checker):
            print_board(board)
            print(f"Player {player} won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
