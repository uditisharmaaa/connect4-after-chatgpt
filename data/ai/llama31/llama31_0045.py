import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D board with the given width and height."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join([chr(65+i) for i in range(BOARD_WIDTH)]))
    print('+---' * BOARD_WIDTH + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * BOARD_WIDTH + '+')

def get_player_input(player):
    """Get the column input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if column in [chr(65+i) for i in range(BOARD_WIDTH)]:
            return ord(column) - 65
        print("Invalid input. Please try again.")

def drop_checker(board, column, checker):
    """Drop the checker into the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break
    else:
        print("Column is full. Turn is lost.")
        return False
    return True

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True

    return False

def play_game():
    """Play the Connect 4 game."""
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        column = get_player_input(current_player)
        if drop_checker(board, column, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if all([all([cell!= ' ' for cell in row]) for row in board]):
                print_board(board)
                print("It's a draw!")
                break
            current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    play_game()
