import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = "XOVHM"

def create_board():
    """Create an empty board with whitespaces."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for cell in row:
            print(cell, end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")

def is_valid_move(board, col):
    """Check if a move is valid (i.e., the column is not full)."""
    return board[0][col] == " "

def get_next_open_row(board, col):
    """Get the next open row in a given column."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row

def drop_piece(board, row, col, checker):
    """Drop a piece into the board at the specified row and column."""
    board[row][col] = checker

def winning_move(board, checker):
    """Check if the given checker has won the game."""
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(cell!= " " for row in board for cell in row)

def main():
    os.system('clear')
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player = random.choice(players)
    print("Player", current_player, "goes first!")

    while True:
        print_board(board)
        col = input("Player " + current_player + ", please enter a column: ").upper()
        if col not in string.ascii_uppercase[:NUM_COLS]:
            print("Invalid input. Please enter a letter between A and", chr(64 + NUM_COLS))
            continue
        col = ord(col) - 65
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_player)

        if winning_move(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
