import os
import random
import string

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, columns):
    """
    Creates a 2D board with the given dimensions, initialized with whitespaces.
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:BOARD_COLUMNS]))
    for row in board:
        print("+---" * BOARD_COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLUMNS + "+")

def is_valid_input(input_str):
    """
    Checks if the input is a single uppercase letter.
    """
    return len(input_str) == 1 and input_str.isalpha() and input_str.isupper()

def is_valid_column(board, column):
    """
    Checks if the column is not full.
    """
    return board[0][column] == " "

def get_player_move(board, player):
    """
    Asks the player for a column and validates the input.
    """
    while True:
        column_str = input(f"Player {player}, please enter a column: ")
        if is_valid_input(column_str):
            column = string.ascii_uppercase.index(column_str)
            if column < BOARD_COLUMNS and is_valid_column(board, column):
                return column
        print("Invalid input. Please try again.")

def place_checker(board, player, column):
    """
    Places the checker in the lowest available space in the column.
    """
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player
            return

def check_win(board, player):
    """
    Checks if the player has won horizontally, vertically, or diagonally.
    """
    # Horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all(cell == player for cell in row[i:i+4]):
                return True
    # Vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all(board[row][col] == player for row in range(i, i+4)):
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """
    Checks if the board is full.
    """
    return all(cell!= " " for row in board for cell in row)

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    current_player = random.choice(players)

    while True:
        print_board(board)
        column = get_player_move(board, current_player)
        place_checker(board, current_player, column)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
