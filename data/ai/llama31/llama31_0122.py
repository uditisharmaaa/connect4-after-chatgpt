import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D board with the specified number of rows and columns."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|   ' + ' |   '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_move(board, col):
    """Check if a move is valid."""
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """Get the next open row in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

def drop_checker(board, row, col, checker):
    """Drop a checker into the specified row and column."""
    board[row][col] = checker

def check_for_win(board, checker):
    """Check if the specified checker has won."""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
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

def check_for_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    # Initialize the game
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    # Game loop
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{string.ascii_uppercase[BOARD_COLS - 1]}):")
        move = input().upper()

        # Validate the move
        if move not in string.ascii_uppercase[:BOARD_COLS]:
            print("Invalid move. Please enter a letter between A and", string.ascii_uppercase[BOARD_COLS - 1])
            continue

        # Get the column number from the move
        col = string.ascii_uppercase.index(move)

        # Check if the move is valid
        if not is_valid_move(board, col):
            print("Invalid move. Column is full.")
            continue

        # Get the next open row
        row = get_next_open_row(board, col)

        # Drop the checker
        drop_checker(board, row, col, current_player)

        # Check for a win
        if check_for_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_for_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch players
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
