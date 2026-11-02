import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2

# Checker characters
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a new Connect 4 board."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the board."""
    print('  A B C D E F G')
    for row in board:
        print('+---' * len(row))
        print('| {} |'.format(' | '.join(row)))
    print('+---' * len(row))

def is_valid_input(column, board):
    """Check if the user's input is valid."""
    if column not in string.ascii_uppercase[:len(board[0])]:
        return False
    column_index = ord(column) - ord('A')
    return board[0][column_index] == ' '

def get_next_open_row(board, column):
    """Get the next open row in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            return board.index(row)
    return -1

def drop_checker(board, column, player):
    """Drop a checker in the specified column."""
    column_index = ord(column) - ord('A')
    row = get_next_open_row(board, column_index)
    if row!= -1:
        board[row][column_index] = CHECKERS[player]

def check_for_win(board, player):
    """Check if the current player has won."""
    checker = CHECKERS[player]
    # Check horizontal locations for win
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_for_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        os.system('clear')
        print_board(board)
        column = input("Player {}, please enter a column (A-{}): ".format(CHECKERS[players[current_player]], string.ascii_uppercase[BOARD_WIDTH - 1]))
        if is_valid_input(column, board):
            drop_checker(board, column, players[current_player])
            if check_for_win(board, players[current_player]):
                os.system('clear')
                print_board(board)
                print("Player {} won!".format(CHECKERS[players[current_player]]))
                break
            elif check_for_draw(board):
                os.system('clear')
                print_board(board)
                print("It's a draw!")
                break
            current_player = (current_player + 1) % len(players)
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
