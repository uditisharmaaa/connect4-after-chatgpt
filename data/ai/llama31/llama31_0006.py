import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the given dimensions"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|', end=' ')
        for cell in row:
            print(f' {cell} |', end=' ')
        print()
    print('+---' * BOARD_COLS + '+')
    print('  A   B   C   D   E   F   G')

def is_valid_move(board, col):
    """Check if a move is valid (i.e., the column is not full)"""
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """Get the next open row in a given column"""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

def make_move(board, col, player):
    """Make a move in a given column"""
    row = get_next_open_row(board, col)
    board[row][col] = CHECKERS[player]

def winning_move(board, player):
    """Check for a winning move"""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row][col + 1] == CHECKERS[player] and board[row][col + 2] == CHECKERS[player] and board[row][col + 3] == CHECKERS[player]:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == CHECKERS[player] and board[row + 1][col] == CHECKERS[player] and board[row + 2][col] == CHECKERS[player] and board[row + 3][col] == CHECKERS[player]:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row + 1][col + 1] == CHECKERS[player] and board[row + 2][col + 2] == CHECKERS[player] and board[row + 3][col + 3] == CHECKERS[player]:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and board[row - 1][col + 1] == CHECKERS[player] and board[row - 2][col + 2] == CHECKERS[player] and board[row - 3][col + 3] == CHECKERS[player]:
                return True

def is_draw(board):
    """Check if the game is a draw"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        move = input().upper()

        # Validate input
        if move not in 'ABCDEFG':
            print("Invalid input. Please enter a column letter.")
            continue

        col = ord(move) - ord('A')
        if not is_valid_move(board, col):
            print("Invalid move. Column is full.")
            continue

        make_move(board, col, current_player)
        print_board(board)

        # Check for win
        if winning_move(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
