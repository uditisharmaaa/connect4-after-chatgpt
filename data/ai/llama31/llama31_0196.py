import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a 2D board with given dimensions"""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board"""
    print("  " + "   ".join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print("+---" * BOARD_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * BOARD_COLS + "+")

def get_player_checker(player_index):
    """Get the checker for a given player"""
    return CHECKERS[player_index % len(CHECKERS)]

def get_valid_input(player_checker):
    """Get a valid column input from the user"""
    while True:
        column = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if column in string.ascii_uppercase[:BOARD_COLS]:
            return column
        print("Invalid input. Please enter a letter between A and", string.ascii_uppercase[BOARD_COLS-1])

def drop_checker(board, column, checker):
    """Drop a checker in the given column"""
    column_index = ord(column) - ord("A")
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return
    print("Column is full. Turn lost.")

def check_win(board, checker):
    """Check if the given checker has won"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == checker:
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= " " for row in board for cell in row)

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, PLAYERS-1)
    while True:
        os.system('clear')
        print_board(board)
        player_checker = get_player_checker(current_player)
        column = get_valid_input(player_checker)
        drop_checker(board, column, player_checker)
        if check_win(board, player_checker):
            os.system('clear')
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
