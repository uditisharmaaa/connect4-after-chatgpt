import os
import random

# Constant variables
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYERS = 2

# List of checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D list filled with whitespace to represent the game board."""
    return [[" " for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board(board):
    """Print the current state of the game board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def get_column_letter():
    """Get a valid column letter from the user."""
    while True:
        letter = input("Enter a column letter (A-{}): ".format(chr(64 + BOARD_WIDTH))).upper()
        if letter >= "A" and letter < chr(65 + BOARD_WIDTH):
            return letter

def drop_checker(board, column, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(BOARD_WIDTH - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical wins
    for col in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
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
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        print("Player {}, please enter a column:".format(current_player))
        column_letter = get_column_letter()
        column = ord(column_letter) - 65
        if board[0][column]!= " ":
            print("Column is full. Try again.")
            input("Press Enter to continue...")
            continue
        drop_checker(board, column, current_player)
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
