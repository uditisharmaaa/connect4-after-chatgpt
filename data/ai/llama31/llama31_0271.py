import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespace."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def validate_input(col, board):
    """Check if the input column is valid."""
    if not col.isalpha():
        return False
    col = ord(col.upper()) - ord('A')
    if col < 0 or col >= BOARD_COLS:
        return False
    if board[0][col]!= ' ':
        return False
    return True

def get_next_open_row(board, col):
    """Find the next open row in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = create_board()
    current_player = random.choice(players)
    os.system('clear')
    print_board(board)
    while True:
        print(f"Player {current_player}, please enter a column:")
        col = input().strip()
        if not validate_input(col, board):
            print("Invalid input. Please try again.")
            continue
        col = ord(col.upper()) - ord('A')
        row = get_next_open_row(board, col)
        if row == -1:
            print("Column is full. Please try again.")
            continue
        board[row][col] = current_player
        os.system('clear')
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
