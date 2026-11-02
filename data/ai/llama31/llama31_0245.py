import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
def initialize_board():
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board

# Print board
def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

# Validate user input
def validate_input(column, board):
    if not column.isalpha() or len(column)!= 1:
        return False
    column = ord(column.upper()) - ord('A')
    if column < 0 or column >= BOARD_COLS:
        return False
    if board[0][column]!= ' ':
        return False
    return True

# Place checker
def place_checker(board, column, player_checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_checker
            return

# Check win
def check_win(board, player_checker):
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == player_checker and row[i+1] == player_checker and row[i+2] == player_checker and row[i+3] == player_checker:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == player_checker and board[i+1][col] == player_checker and board[i+2][col] == player_checker and board[i+3][col] == player_checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row+1][col+1] == player_checker and board[row+2][col+2] == player_checker and board[row+3][col+3] == player_checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row-1][col+1] == player_checker and board[row-2][col+2] == player_checker and board[row-3][col+3] == player_checker:
                return True

    return False

# Main game loop
def main():
    num_players = 2
    players = CHECKERS[:num_players]
    board = initialize_board()
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f'Player {current_player}, please enter a column:')
        column = input().strip()

        if not validate_input(column, board):
            print('Invalid input. Please try again.')
            continue

        column = ord(column.upper()) - ord('A')
        place_checker(board, column, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f'Player {current_player} won!')
            break

        # Check for draw
        if all(all(cell!= ' ' for cell in row) for row in board):
            print_board(board)
            print('It\'s a draw!')
            break

        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == '__main__':
    main()
