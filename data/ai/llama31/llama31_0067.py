import os
import random

# Constant global variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D board with whitespaces"""
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

def print_board(board):
    """Print the board with column labels"""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_index):
    """Get the checker for the current player"""
    return CHECKERS[player_index]

def get_column_from_input(input_str):
    """Convert input string to column index"""
    return ord(input_str.upper()) - ord('A')

def is_valid_input(input_str, board):
    """Check if input is a valid column letter and not full"""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    column_index = get_column_from_input(input_str)
    if column_index < 0 or column_index >= BOARD_COLUMNS:
        return False
    return board[0][column_index] == " "

def get_player_move(player_checker, board):
    """Get a valid move from the player"""
    while True:
        print("Player {}, please enter a column:".format(player_checker))
        input_str = input()
        if is_valid_input(input_str, board):
            return get_column_from_input(input_str)

def drop_checker(board, column_index, player_checker):
    """Drop the checker into the column"""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column_index] == " ":
            board[row_index][column_index] = player_checker
            return

def check_win(board, player_checker):
    """Check for a win horizontally, vertically, or diagonally"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == player_checker:
                return True
    # Check vertical
    for col in range(BOARD_COLUMNS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == player_checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player_checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player_checker:
                return True
    return False

def check_draw(board):
    """Check if the board is full"""
    return all(cell!= " " for row in board for cell in row)

def main():
    board = create_board()
    players = [get_player_checker(i) for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        player_checker = players[current_player_index]
        column_index = get_player_move(player_checker, board)
        drop_checker(board, column_index, player_checker)
        if check_win(board, player_checker):
            print_board(board)
            print("Player {} won!".format(player_checker))
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
