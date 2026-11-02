import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
CHECKERS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

def create_board():
    """Create a new Connect 4 board"""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the Connect 4 board"""
    print("  A B C D E F G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} |".format(" | ".join(row)))
    print("+---+---+---+---+---+---+---+")

def is_valid_move(board, col):
    """Check if a move is valid"""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Get the next open row in a column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def drop_checker(board, col, checker):
    """Drop a checker into a column"""
    row = get_next_open_row(board, col)
    board[row][col] = checker

def winning_move(board, checker):
    """Check for a winning move"""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def game_over(board):
    """Check if the game is over"""
    for col in range(BOARD_COLS):
        if board[0][col] == " ":
            return False
    return True

def main():
    # Create a new board
    board = create_board()

    # Choose a random first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Game loop
    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Get the current player's checker
        current_checker = CHECKERS[current_player]

        # Get the player's move
        while True:
            move = input("Player {}, please enter a column (A-{}): ".format(current_checker, chr(65 + BOARD_COLS - 1)))
            if move.upper() < 'A' or move.upper() > chr(65 + BOARD_COLS - 1):
                print("Invalid move, try again.")
            else:
                col = ord(move.upper()) - 65
                if is_valid_move(board, col):
                    break
                else:
                    print("Column is full, try again.")

        # Drop the checker
        drop_checker(board, col, current_checker)

        # Check for a win
        if winning_move(board, current_checker):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(current_checker))
            break

        # Check for a draw
        if game_over(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
