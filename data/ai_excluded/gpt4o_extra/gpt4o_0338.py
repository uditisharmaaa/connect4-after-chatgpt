import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for up to 5 players
PLAYER_COUNT = 2  # Number of players
EMPTY_CELL = " "

# Initialize the board
def create_board():
    return [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

# Print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Check if the move is valid
def is_valid_move(board, column):
    return 0 <= column < COLS and board[0][column] == EMPTY_CELL

# Get the next open row in a column
def get_next_open_row(board, column):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == EMPTY_CELL:
            return r
    return None

# Place the piece on the board
def place_checker(board, row, column, checker):
    board[row][column] = checker

# Check for a win condition
def check_for_win(board, player):
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

# Check if the board is full
def is_board_full(board):
    return all(board[0][c] != EMPTY_CELL for c in range(COLS))

def main():
    board = create_board()
    print_board(board)
    
    # Randomly select the first player
    current_player = random.randint(0, PLAYER_COUNT - 1)
    players = PLAYER_SYMBOLS[:PLAYER_COUNT]

    while True:
        print(f"Player {players[current_player]}, please enter a column (A-G):")
        column_input = input().strip().upper()

        if len(column_input) != 1 or not ('A' <= column_input <= chr(65 + COLS - 1)):
            print("Invalid input, please enter a valid column letter.")
            continue

        column = ord(column_input) - 65

        if not is_valid_move(board, column):
            print("Column is full or invalid move.")
            continue

        row = get_next_open_row(board, column)
        place_checker(board, row, column, players[current_player])

        print_board(board)

        if check_for_win(board, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break

        if is_board_full(board):
            print("It's a draw!")
            break
       
        # Alternate turn
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == '__main__':
    main()
