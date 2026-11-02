import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} |'.format(' | '.join(row)))
    print('+---+---+---+---+---+---+---+')

# Check if the input is valid
def is_valid_input(board, col):
    return board[0][col] == ' '

# Get the player's move
def get_player_move(player, board):
    while True:
        move = input('Player {}, please enter a column: '.format(player)).upper()
        if move in 'ABCDEFG' and board[0][ord(move) - 65] == ' ':
            return ord(move) - 65
        else:
            print('Invalid input. Please try again.')

# Place the checker in the correct location
def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == player:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == player:
                return True

    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True
            if board[row][col+3] == board[row+1][col+2] == board[row+2][col+1] == board[row+3][col] == player:
                return True

    return False

# Main game loop
def play_game():
    num_players = 2
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    while True:
        print_board(board)
        col = get_player_move(current_player, board)
        place_checker(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print('Player {} won!'.format(current_player))
            break

        if ' ' not in [item for sublist in board for item in sublist]:
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = players[(players.index(current_player) + 1) % num_players]

play_game()
