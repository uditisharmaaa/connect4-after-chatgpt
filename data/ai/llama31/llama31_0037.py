import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_PLAYERS = len(CHECKERS)

def create_board(rows, cols):
    """Create an empty board with the given dimensions."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:NUM_COLS]))
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

def is_valid_move(board, col):
    """Check if a move is valid."""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Get the next open row in a column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def check_win(board, checker):
    """Check for a win condition."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print_board(board)
    print("Player", current_player, "starts.")

    while True:
        print("Player", current_player, "turn:")
        col = input("Enter column (A-{}): ".format(string.ascii_uppercase[NUM_COLS - 1])).upper()
        if col not in string.ascii_uppercase[:NUM_COLS]:
            print("Invalid column. Please try again.")
            continue
        col = string.ascii_uppercase.index(col)

        if not is_valid_move(board, col):
            print("Column is full. Please try again.")
            continue

        row = get_next_open_row(board, col)
        board[row][col] = current_player
        print_board(board)

        if check_win(board, current_player):
            print("Player", current_player, "won!")
            break

        if all([cell!= " " for row in board for cell in row]):
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
