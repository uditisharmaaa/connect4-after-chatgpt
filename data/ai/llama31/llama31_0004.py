import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_num):
    """Return the checker symbol for the given player number."""
    return CHECKERS[player_num - 1]

def get_column_index(column):
    """Return the column index for the given column letter."""
    return ord(column.upper()) - ord('A')

def is_valid_column(column):
    """Return True if the column is within the board bounds."""
    return 'A' <= column.upper() <= chr(ord('A') + BOARD_COLS - 1)

def is_column_full(board, column):
    """Return True if the column is full."""
    return board[0][get_column_index(column)]!= ' '

def get_next_open_row(board, column):
    """Return the next open row in the column."""
    for row in reversed(board):
        if row[get_column_index(column)] == ' ':
            return board.index(row)

def drop_checker(board, column, checker):
    """Drop the checker into the column."""
    row = get_next_open_row(board, column)
    board[row][get_column_index(column)] = checker

def check_win(board, checker):
    """Return True if the given checker has won."""
    # Check horizontal locations for win
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS):
            if board[r][c] == checker and board[r][c + 1] == checker and board[r][c + 2] == checker and board[r][c + 3] == checker:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c] == checker and board[r + 2][c] == checker and board[r + 3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(BOARD_ROWS - 3):
            if board[r][c] == checker and board[r + 1][c + 1] == checker and board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS - 3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == checker and board[r - 1][c + 1] == checker and board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker:
                return True

def check_draw(board):
    """Return True if the board is full and no player has won."""
    return all(all(cell!= ' ' for cell in row) for row in board)

def main():
    board = create_board()
    players = [get_player_checker(i) for i in range(1, NUM_PLAYERS + 1)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board)
        print('Player {}, please enter a column:'.format(players[current_player_index]))
        column = input()
        if not is_valid_column(column) or is_column_full(board, column):
            print('Invalid input. Please try again.')
            continue
        drop_checker(board, column, players[current_player_index])
        if check_win(board, players[current_player_index]):
            os.system('clear')
            print_board(board)
            print('Player {} won!'.format(players[current_player_index]))
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print('It\'s a draw!')
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
