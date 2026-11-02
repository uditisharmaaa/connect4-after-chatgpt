import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to create the board
def create_board():
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  A", end="")
    for col in range(1, BOARD_COLS):
        print("  {}".format(chr(ord('A') + col)), end="")
    print("\n" + "+" + "---+" * BOARD_COLS)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            print("| {} ".format(board[row][col]), end="")
        print("|")
        print("+" + "---+" * BOARD_COLS)

# Function to check for valid input
def is_valid_input(col):
    if len(col)!= 1:
        return False
    if not col.isalpha():
        return False
    if ord(col.upper()) - ord('A') < 0 or ord(col.upper()) - ord('A') >= BOARD_COLS:
        return False
    return True

# Function to get the column number from the input
def get_col_num(col):
    return ord(col.upper()) - ord('A')

# Function to check if the column is full
def is_col_full(board, col):
    return board[0][col]!= " "

# Function to place the checker
def place_checker(board, player, col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

# Main function
def main():
    board = create_board()
    players = random.sample(CHECKERS, PLAYERS)
    current_player = random.choice(players)

    while True:
        print_board(board)
        print("Player {}, please enter a column:".format(current_player))
        col = input().strip()

        if not is_valid_input(col):
            print("Invalid input. Please try again.")
            continue

        col_num = get_col_num(col)

        if is_col_full(board, col_num):
            print("Column is full. Please try again.")
            continue

        place_checker(board, current_player, col_num)

        if check_win(board, current_player):
            print_board(board)
            print("Player {} won!".format(current_player))
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
