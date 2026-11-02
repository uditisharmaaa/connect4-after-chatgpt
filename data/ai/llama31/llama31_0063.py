import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(columns, rows):
    """Create a 2D board with the given dimensions"""
    board = []
    for _ in range(rows):
        row = [" "] * columns
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board"""
    columns = ["A", "B", "C", "D", "E", "F", "G"]
    os.system('clear')
    print("  ", end="")
    for col in range(BOARD_COLUMNS):
        print(columns[col], end="   ")
    print()
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLUMNS + "+")
        print("|", end="")
        for col in range(BOARD_COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * BOARD_COLUMNS + "+")

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return input_str.upper() in [chr(i) for i in range(ord('A'), ord('A') + BOARD_COLUMNS)]

def get_column_index(input_str):
    """Convert the input letter to a column index"""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, column_index):
    """Check if the given column is full"""
    return board[0][column_index]!= " "

def get_next_available_row(board, column_index):
    """Get the next available row in the given column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return -1

def place_checker(board, column_index, checker):
    """Place the checker in the given column"""
    row = get_next_available_row(board, column_index)
    if row == -1:
        return False
    board[row][column_index] = checker
    return True

def check_win(board, checker):
    """Check if the given player has won"""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board(BOARD_COLUMNS, BOARD_ROWS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        print("Player", current_player, "please enter a column:")
        input_str = input()
        if not is_valid_input(input_str):
            print("Invalid input. Please enter a column letter.")
            continue
        column_index = get_column_index(input_str)
        if is_column_full(board, column_index):
            print("Column is full. Please choose another column.")
            continue
        if not place_checker(board, column_index, current_player):
            print("Failed to place checker. Please try again.")
            continue
        if check_win(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
