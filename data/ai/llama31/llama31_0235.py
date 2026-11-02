import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Create the game board
def create_board():
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(' ')
        board.append(row)
    return board

# Print the game board
def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---' * BOARD_COLS + '+')

# Validate user input
def validate_input(column, board):
    if not column.isalpha() or not column.upper() in 'ABCDEFG':
        return False
    column = ord(column.upper()) - 65
    if board[0][column]!= ' ':
        return False
    return True

# Get the next available row
def get_next_row(column, board):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positive diagonal
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negative diagonal
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

# Main game loop
def main():
    board = create_board()
    players = PLAYERS[:2]  # Set the number of players to 2
    current_player = random.choice(players)
    while True:
        print_board(board)
        print(f'Player {current_player}, please enter a column:')
        column = input().lower()
        while not validate_input(column, board):
            print('Invalid input. Please try again.')
            column = input().lower()
        column = ord(column.upper()) - 65
        row = get_next_row(column, board)
        board[row][column] = current_player
        if check_win(board, current_player):
            print_board(board)
            print(f'Player {current_player} won!')
            break
        if all(cell!= ' ' for row in board for cell in row):
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == '__main__':
    main()
