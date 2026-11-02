import os
import random
import string

# Constant variables
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the board
def create_board(rows, cols):
    """Create a 2D board with the given dimensions"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    """Print the board in a human-readable format"""
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

# Function to check for a win
def check_win(board, player):
    """Check if the given player has won the game"""
    # Check horizontal wins
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == player:
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    """Check if the game is a draw"""
    return all(cell!= ' ' for row in board for cell in row)

# Main game loop
def play_game():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        while True:
            try:
                col = input().strip().upper()
                if col not in string.ascii_uppercase[:BOARD_COLS]:
                    raise ValueError
                col = string.ascii_uppercase.index(col)
                if all(cell!= ' ' for cell in [board[row][col] for row in range(BOARD_ROWS)]):
                    print("Column is full, try again.")
                    continue
                for row in reversed(board):
                    if row[col] == ' ':
                        row[col] = current_player
                        break
                break
            except (IndexError, ValueError):
                print("Invalid input, try again.")

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

play_game()
