import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates an empty board with the given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| {} |'.format(' | '.join(row)))
    print('+---' * BOARD_COLS + '+')

def get_valid_move(board, player):
    """Asks the player for a column and validates the input."""
    while True:
        column = input("Player {}, please enter a column: ".format(player)).upper()
        if column not in 'ABCDEFG':
            print("Invalid column. Please enter a letter between A and G.")
        elif board[0][ord(column) - ord('A')]!= ' ':
            print("Column is full. Please choose another column.")
        else:
            return ord(column) - ord('A')

def make_move(board, player, column):
    """Places the player's checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            break

def check_win(board, player):
    """Checks if the given player has won."""
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

def check_draw(board):
    """Checks if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def play_game():
    """Starts a new game of Connect 4."""
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    print("Randomly selected player: {}".format(current_player))

    while True:
        print_board(board)
        column = get_valid_move(board, current_player)
        make_move(board, current_player, column)
        if check_win(board, current_player):
            print_board(board)
            print("Player {} won!".format(current_player))
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

play_game()
