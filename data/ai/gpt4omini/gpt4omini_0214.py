import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']

def create_board():
    """Initialize the Connect 4 board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join([chr(65 + c) for c in range(COLS)]))  # Column labels A, B, C, ...
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def get_next_open_row(board, col):
    """Return the next available row in the specified column."""
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1  # If column is full

def is_valid_location(board, col):
    """Check if the specified column has space for a checker."""
    return board[0][col] == " "

def place_piece(board, row, col, piece):
    """Place a piece on the board."""
    board[row][col] = piece

def winning_move(board, piece):
    """Check if the specified piece has won."""
    # Check all horizontal locations
    for c in range(COLS-3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Check all vertical locations
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Check positively sloped diagonals
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full, indicating a draw."""
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    game_over = False
    turn = random.randint(0, len(PLAYERS) - 1)

    print_board(board)

    while not game_over:
        player = PLAYERS[turn]
        col = -1

        while col < 0 or col >= COLS or not is_valid_location(board, col):
            try:
                col_input = input(f"Player {player}, please enter a column (A-G): ").upper()
                col = ord(col_input) - 65  # Convert letter to column index
            except (ValueError, IndexError):
                col = -1  # Reset col to invalid if there's an error

        row = get_next_open_row(board, col)
        if row != -1:
            place_piece(board, row, col, player)

            if winning_move(board, player):
                print_board(board)
                print(f"Player {player} won!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                turn = (turn + 1) % len(PLAYERS)  # Switch turns

        print_board(board)

if __name__ == "__main__":
    main()
