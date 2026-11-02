import os
import random

# Constant variables
NUM_ROWS = 6
NUM_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with all elements initialized to whitespaces"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board"""
    print('  A', end='')
    for col in range(1, NUM_COLS):
        print(' ', chr(ord('A') + col), end='')
    print()
    for row in range(NUM_ROWS):
        print('+---' * NUM_COLS + '+')
        print('|', end='')
        for col in range(NUM_COLS):
            print(' ' + board[row][col] + ' |', end='')
        print()
    print('+---' * NUM_COLS + '+')

def get_player_input(player, board):
    """Get and validate the player's input"""
    while True:
        col = input("Player " + player + ", please enter a column: ")
        if len(col)!= 1 or not col.isalpha() or not 'A' <= col <= 'G':
            print("Invalid input. Please enter a letter from A to G.")
        elif board[0][ord(col) - ord('A')]!= ' ':
            print("Column is full. Please choose another column.")
        else:
            return ord(col) - ord('A')

def place_checker(board, player, col):
    """Place the checker in the lowest available space in the column"""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            break

def check_win(board, player):
    """Check if the player has won"""
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    # Create the board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Set the number of players
    num_players = 2

    # Choose a random player to start
    current_player = random.randint(0, num_players - 1)

    # Game loop
    while True:
        os.system('clear')
        print_board(board)

        # Get the player's input
        col = get_player_input(CHECKERS[current_player], board)

        # Place the checker
        place_checker(board, CHECKERS[current_player], col)

        # Check if the player has won
        if check_win(board, CHECKERS[current_player]):
            os.system('clear')
            print_board(board)
            print("Player " + CHECKERS[current_player] + " won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
