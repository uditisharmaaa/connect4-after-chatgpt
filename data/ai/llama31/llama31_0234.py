import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the given dimensions."""
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print('   ' + chr(ord('A') + col), end='')
    print('\n+' + '+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS - 1, -1, -1):
        print('|', end='')
        for col in range(BOARD_COLS):
            print(' ' + board[row][col] + ' |', end='')
        print('\n+' + '+---' * BOARD_COLS + '+')
    print()

def is_valid_move(board, col):
    """Check if the given column is a valid move."""
    return board[BOARD_ROWS - 1][col] == ' '

def make_move(board, player, col):
    """Make a move in the given column."""
    for row in range(BOARD_ROWS):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the given player has won."""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        col = input().upper()
        if not col.isalpha() or not 'A' <= col <= chr(ord('A') + BOARD_COLS - 1):
            print("Invalid input. Please try again.")
            continue
        col = ord(col) - ord('A')
        if not is_valid_move(board, col):
            print("Column is full. Please try again.")
            continue
        make_move(board, current_player, col)
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
