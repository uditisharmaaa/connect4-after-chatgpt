import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---+---+---+---+---+---+---+')

def get_valid_move(board, column):
    """Get the first empty row in the given column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return -1

def check_win(board, player):
    """Check for a win in all directions (horizontally, vertically, diagonally)."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == player:
                # Check horizontal
                if col < BOARD_COLS - 3:
                    if board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                        return True
                # Check vertical
                if row < BOARD_ROWS - 3:
                    if board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                        return True
                # Check diagonal (top-left to bottom-right)
                if row < BOARD_ROWS - 3 and col < BOARD_COLS - 3:
                    if board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                        return True
                # Check diagonal (bottom-left to top-right)
                if row > 2 and col < BOARD_COLS - 3:
                    if board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                        return True
    return False

def check_draw(board):
    """Check if the board is full (i.e., it's a draw)."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    # Initialize the board
    board = create_board()

    # Randomly select the first player
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)

    while True:
        # Clear the screen
        os.system('clear')

        # Print the board
        print_board(board)

        # Ask the current player for their move
        print(f"Player {current_player}, please enter a column (A-{chr(64 + BOARD_COLS)}):")
        move = input().upper()

        # Validate the move
        if move < 'A' or move > chr(64 + BOARD_COLS):
            print("Invalid column. Please try again.")
            continue

        # Convert the move to a column index
        column = ord(move) - 65

        # Get the first empty row in the column
        row = get_valid_move(board, column)
        if row == -1:
            print("Column is full. Please try again.")
            continue

        # Place the checker
        board[row][column] = current_player

        # Check for a win
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        players.remove(current_player)
        current_player = players[0]
        players.append(current_player)

if __name__ == "__main__":
    main()
