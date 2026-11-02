import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with whitespace elements"""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_num):
    """Get the checker symbol for the given player number"""
    return CHECKERS[player_num - 1]

def is_valid_input(col):
    """Check if the user input is a valid column letter"""
    return col.upper() >= 'A' and col.upper() <= chr(ord('A') + NUM_COLS - 1)

def get_col_index(col):
    """Convert a column letter to a zero-based index"""
    return ord(col.upper()) - ord('A')

def drop_checker(board, col, checker):
    """Drop the checker into the given column"""
    for row in reversed(board):
        if row[get_col_index(col)] == ' ':
            row[get_col_index(col)] = checker
            return

def check_win(board):
    """Check for a win in any direction (horizontal, vertical, diagonal)"""
    # Horizontal
    for row in board:
        for i in range(NUM_COLS - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3]!= ' ':
                return True
    # Vertical
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col]!= ' ':
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]!= ' ':
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]!= ' ':
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)"""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    players = list(range(1, NUM_PLAYERS + 1))
    random.shuffle(players)  # Randomly select first player
    current_player = 0

    while True:
        os.system('clear')
        print_board(board)
        player_num = players[current_player]
        checker = get_player_checker(player_num)
        print(f"Player {checker}, please enter a column: ", end='')
        col = input().strip()

        while not is_valid_input(col):
            print("Invalid input. Please enter a column letter: ", end='')
            col = input().strip()

        drop_checker(board, col, checker)

        if check_win(board):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
