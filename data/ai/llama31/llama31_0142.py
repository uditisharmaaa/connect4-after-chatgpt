import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a new board with the given width and height."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A', end='')
    for i in range(1, BOARD_WIDTH):
        print('  ' + chr(ord('A') + i), end='')
    print('\n+---' + '+---' * (BOARD_WIDTH - 1) + '+')
    for row in board:
        print('|', end='')
        for cell in row:
            print(' ' + cell + ' |', end='')
        print('\n+---' + '+---' * (BOARD_WIDTH - 1) + '+')

def is_valid_input(input_str, width):
    """Check if the input is a valid column letter."""
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    col_num = ord(input_str.upper()) - ord('A')
    return 0 <= col_num < width

def is_valid_move(board, col):
    """Check if the move is valid (column is not full)."""
    return board[0][col] == ' '

def make_move(board, player, col):
    """Make a move by placing the checker in the given column."""
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            break

def check_win(board, player):
    """Check if the given player has won."""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == player for cell in row[i:i+4]]):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == player for row in range(i, i+4)]):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == player for i in range(4)]):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == player for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all([cell!= ' ' for row in board for cell in row])

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        input_str = input().strip()

        if not is_valid_input(input_str, BOARD_WIDTH):
            print("Invalid input. Please enter a column letter.")
            continue

        col = ord(input_str.upper()) - ord('A')
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue

        make_move(board, current_player, col)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
