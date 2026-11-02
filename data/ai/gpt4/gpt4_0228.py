import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players
COLUMN_HEADERS = [chr(65 + i) for i in range(COLS)]  # ['A', 'B', 'C', ..., 'G']


def initialize_board(rows, cols):
    """Initialize the game board."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the screen
    print('  ' + '   '.join(COLUMN_HEADERS))
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')


def get_player_column_input():
    """Prompt the player for input and validate against allowed columns."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        if len(column) == 1 and column in COLUMN_HEADERS:
            return COLUMN_HEADERS.index(column)
        print("Invalid input. Please enter a valid column (A-G).")


def place_checker(board, column, checker):
    """Place a checker in the selected column, returns success status."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full


def check_win(board, row, col, checker):
    """Check if the player has won after placing a checker."""
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],  # Vertical
        [(1, 1), (-1, -1)],  # Diagonal /
        [(1, -1), (-1, 1)]  # Diagonal \
    ]

    for direction in directions:
        count = 1
        for dx, dy in direction:
            r, c = row, col
            while True:
                r += dx
                c += dy
                if r < 0 or r >= ROWS or c < 0 or c >= COLS or board[r][c] != checker:
                    break
                count += 1
            if count >= 4:
                return True
    return False


def check_draw(board):
    """Check if the game is a draw."""
    return all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLS))


def find_last_placed_row(board, column):
    """Find the last occupied row in a column."""
    for row in range(ROWS):
        if board[row][column] != ' ':
            return row
    return -1


def main():
    # Initialize Board
    board = initialize_board(ROWS, COLS)
    
    # Randomly determine the starting player
    current_player = random.randint(0, PLAYERS - 1)

    # Print the initial board
    print_board(board)

    # Start the game cycle
    while True:
        print(f"Player {CHECKERS[current_player]}'s turn.")
        column = get_player_column_input()
        
        # Attempt to place the checker
        if place_checker(board, column, CHECKERS[current_player]):
            # Determine the row of the last placed checker
            row = find_last_placed_row(board, column)
            
            # Check for win
            if check_win(board, row, column, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                break
            
            # Check for draw
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            # Switch player turn
            current_player = (current_player + 1) % PLAYERS

        else:
            print(f"Column {COLUMN_HEADERS[column]} is full. Try again.")

        print_board(board)


if __name__ == "__main__":
    main()
