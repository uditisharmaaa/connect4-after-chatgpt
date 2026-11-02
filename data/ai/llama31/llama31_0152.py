import os
import random

# Constants
NUM_PLAYERS = 2
NUM_COLUMNS = 7
NUM_ROWS = 6

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(NUM_COLUMNS)))
    print('+' + '+---' * NUM_COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(cell + ' ' for cell in row) + '|')
        print('+' + '+---' * NUM_COLUMNS + '+')

# Get the player's move
def get_player_move(player):
    while True:
        move = input(f'Player {CHECKERS[player]}, please enter a column: ').strip().upper()
        if move.isalpha() and 0 <= ord(move) - 65 < NUM_COLUMNS:
            return ord(move) - 65
        print('Invalid move. Please try again.')

# Place the player's checker
def place_checker(board, player, column):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = CHECKERS[player]
            return
    print('Column is full. Please try again.')

# Check for a win
def check_win(board):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i]!= ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col]!= ' ' and board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col]:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col]!= ' ' and board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col]!= ' ' and board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell!= ' ' for row in board for cell in row)

# Main game loop
def main():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        column = get_player_move(players[current_player])
        place_checker(board, players[current_player], column)

        if check_win(board):
            print_board(board)
            print(f'Player {CHECKERS[players[current_player]]} won!')
            break

        if check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
