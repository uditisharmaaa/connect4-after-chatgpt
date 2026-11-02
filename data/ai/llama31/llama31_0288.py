import os
import random

# Constant global variables
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """
    Creates a 2D board with the given dimensions and initializes all elements with whitespaces.
    """
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board, player):
    """
    Prints the current state of the board.
    """
    os.system('clear')
    print("  A", end="")
    for col in range(1, BOARD_COLS):
        print("   " + chr(ord('A') + col), end="")
    print()
    for row in range(BOARD_ROWS):
        print("+---", end="")
        for _ in range(BOARD_COLS):
            print("+---", end="")
        print("+")
        print("|   ", end="")
        for col in range(BOARD_COLS):
            print("| " + board[row][col] + " ", end="")
        print("|   ")
    print("+---", end="")
    for _ in range(BOARD_COLS):
        print("+---", end="")
    print("+")
    print("Player " + CHECKERS[player] + ", please enter a column:")

def validate_input(col, board):
    """
    Checks if the input column is valid.
    """
    if not col.isalpha():
        return False
    col = ord(col.upper()) - ord('A')
    if col < 0 or col >= BOARD_COLS:
        return False
    if board[0][col]!= " ":
        return False
    return True

def place_checker(board, col, player):
    """
    Places the checker in the given column.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[player]
            return

def check_win(board, player):
    """
    Checks if the given player has won.
    """
    checker = CHECKERS[player]
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """
    Checks if the game is a draw.
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def main():
    board = create_board()
    players = [i for i in range(PLAYERS)]
    random.shuffle(players)
    current_player = 0
    while True:
        print_board(board, current_player)
        col = input().upper()
        while not validate_input(col, board):
            print("Invalid input. Please try again.")
            col = input().upper()
        place_checker(board, ord(col) - ord('A'), current_player)
        if check_win(board, current_player):
            print_board(board, current_player)
            print("Player " + CHECKERS[current_player] + " won!")
            break
        elif check_draw(board):
            print_board(board, current_player)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
