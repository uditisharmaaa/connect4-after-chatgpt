import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board(rows, cols):
    """
    Create an empty board with the specified number of rows and columns.
    """
    board = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    """
    Print the current state of the board.
    """
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")

def get_player_checker(player_index):
    """
    Get the checker symbol for the specified player.
    """
    return PLAYERS[player_index]

def is_valid_input(column):
    """
    Check if the user input is a valid column letter.
    """
    return 'A' <= column <= 'G' and column == column.upper()

def get_column_index(column):
    """
    Convert the column letter to an index.
    """
    return ord(column) - ord('A')

def is_valid_move(board, column):
    """
    Check if the specified column is not full.
    """
    return board[0][column] == " "

def make_move(board, player_index, column):
    """
    Place the player's checker in the specified column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = get_player_checker(player_index)
            return

def check_win(board, player_index):
    """
    Check if the player has won by looking for four consecutive checkers.
    """
    checker = get_player_checker(player_index)
    # Check horizontal wins
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical wins
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def is_draw(board):
    """
    Check if the game is a draw by looking for any empty cells.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)  # Randomly select the first player
    current_player_index = 0
    while True:
        print_board(board)
        column = input("Player " + get_player_checker(players[current_player_index]) + ", please enter a column: ")
        if not is_valid_input(column):
            print("Invalid input. Please try again.")
            continue
        column_index = get_column_index(column)
        if not is_valid_move(board, column_index):
            print("Column is full. Please try again.")
            continue
        make_move(board, players[current_player_index], column_index)
        if check_win(board, players[current_player_index]):
            print_board(board)
            print("Player " + get_player_checker(players[current_player_index]) + " won!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
