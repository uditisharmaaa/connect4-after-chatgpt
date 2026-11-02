import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the game board
def create_board():
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Function to print the game board
def print_board(board, current_player):
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')
    print(f'Player {CHECKERS[current_player]}, please enter a column: ')

# Function to validate user input
def validate_input(column, board):
    try:
        column = ord(column.upper()) - 65
        if column < 0 or column >= COLS:
            return False
        for row in reversed(board):
            if row[column] == ' ':
                return True
    except ValueError:
        return False
    return False

# Function to place a checker on the board
def place_checker(column, board, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = CHECKERS[player]
            return

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for row in board:
        for i in range(COLS - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == CHECKERS[player]:
                return True

    # Check vertical
    for col in range(COLS):
        for i in range(ROWS - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == CHECKERS[player]:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == CHECKERS[player]:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == CHECKERS[player]:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Main game loop
def main():
    board = create_board()
    players = random.sample(range(PLAYERS), PLAYERS)
    current_player = 0

    while True:
        print_board(board, current_player)
        column = input().strip()
        if not validate_input(column, board):
            print('Invalid input. Please try again.')
            continue
        column = ord(column.upper()) - 65
        place_checker(column, board, players[current_player])
        if check_win(board, players[current_player]):
            print_board(board, current_player)
            print(f'Player {CHECKERS[players[current_player]]} won!')
            break
        elif check_draw(board):
            print_board(board, current_player)
            print('It\'s a draw!')
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
