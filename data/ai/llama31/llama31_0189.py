import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

# Check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == ' '

# Get the next available row in a column
def get_next_row(board, col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row

# Place a checker in a column
def place_checker(board, player, col):
    row = get_next_row(board, col)
    board[row][col] = player

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Main game loop
def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    players.remove(current_player)
    players.insert(0, current_player)

    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-{string.ascii_uppercase[BOARD_COLS - 1]}):")
        col = input().upper()
        col = string.ascii_uppercase.index(col)

        if not is_valid_move(board, col):
            print("Invalid move, please try again.")
            continue

        place_checker(board, current_player, col)

        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
