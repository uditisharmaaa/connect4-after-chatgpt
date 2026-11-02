import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = "XOVHM"

def create_board():
    """Create a 2D board with the specified dimensions"""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print("  A", end="")
    for col in range(1, COLUMNS):
        print(" |", chr(65 + col), end="")
    print(" |\n+" + "---+" * COLUMNS)
    for row in range(ROWS):
        for col in range(COLUMNS):
            print(" |", board[row][col], end="")
        print(" |\n+" + "---+" * COLUMNS)

def get_player_checker(player_index):
    """Get the checker symbol for the current player"""
    return CHECKERS[player_index]

def is_valid_input(input_str):
    """Check if the user input is a valid column letter"""
    return input_str.isalpha() and input_str.upper() in string.ascii_uppercase[:COLUMNS]

def get_column_index(input_str):
    """Get the column index from the user input"""
    return ord(input_str.upper()) - 65

def is_valid_move(board, column):
    """Check if the move is valid (column is not full)"""
    return board[0][column] == " "

def make_move(board, column, checker):
    """Make a move by placing the checker in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = 0
    while True:
        print_board(board)
        player_checker = get_player_checker(players[current_player])
        while True:
            input_str = input("Player {}, please enter a column: ".format(player_checker))
            if is_valid_input(input_str):
                column = get_column_index(input_str)
                if is_valid_move(board, column):
                    make_move(board, column, player_checker)
                    break
                else:
                    print("Invalid move, column is full. Try again.")
            else:
                print("Invalid input. Please enter a letter from A to G.")
        if check_win(board, player_checker):
            print_board(board)
            print("Player {} won!".format(player_checker))
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
