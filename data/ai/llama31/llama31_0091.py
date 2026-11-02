import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with all elements initialized to whitespace."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A', ' B', ' C', ' D', ' E', ' F', ' G')
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|', end=' ')
        for cell in row:
            print(cell, end=' | ')
        print()
    print('+---' * NUM_COLS + '+')

def get_valid_input():
    """Get a valid column input from the user."""
    while True:
        user_input = input("Enter a column (A-G): ").strip().upper()
        if user_input in 'ABCDEFG':
            col_index = ord(user_input) - ord('A')
            if col_index < NUM_COLS:
                return col_index
        print("Invalid input. Please try again.")

def drop_checker(board, col_index, checker):
    """Drop a checker into the specified column."""
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = checker
            return

def check_win(board, checker):
    """Check if the specified checker has won."""
    # Check horizontal wins
    for row in board:
        for col_index in range(NUM_COLS - 3):
            if row[col_index] == checker and row[col_index + 1] == checker and row[col_index + 2] == checker and row[col_index + 3] == checker:
                return True

    # Check vertical wins
    for col_index in range(NUM_COLS):
        for row_index in range(NUM_ROWS - 3):
            if board[row_index][col_index] == checker and board[row_index + 1][col_index] == checker and board[row_index + 2][col_index] == checker and board[row_index + 3][col_index] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row_index in range(NUM_ROWS - 3):
        for col_index in range(NUM_COLS - 3):
            if board[row_index][col_index] == checker and board[row_index + 1][col_index + 1] == checker and board[row_index + 2][col_index + 2] == checker and board[row_index + 3][col_index + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row_index in range(3, NUM_ROWS):
        for col_index in range(NUM_COLS - 3):
            if board[row_index][col_index] == checker and board[row_index - 1][col_index + 1] == checker and board[row_index - 2][col_index + 2] == checker and board[row_index - 3][col_index + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (i.e., the board is full)."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}, please enter a column:")
        col_index = get_valid_input()
        if board[0][col_index]!= ' ':
            print("Column is full. Please try again.")
            continue
        drop_checker(board, col_index, players[current_player_index])
        if check_win(board, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
