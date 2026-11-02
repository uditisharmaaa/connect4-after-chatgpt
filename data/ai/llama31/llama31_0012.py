import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty Connect 4 board"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_index):
    """Get the checker for the given player index"""
    return CHECKERS[player_index]

def is_valid_input(input_str):
    """Check if the input is a valid column letter"""
    return input_str.upper() in 'ABCDEFG'

def get_column_index(input_str):
    """Get the column index from the input string"""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, col_index):
    """Check if the column is full"""
    return board[0][col_index]!= ' '

def get_next_available_row(board, col_index):
    """Get the next available row in the column"""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            return row_index
    return -1

def place_checker(board, player_checker, col_index):
    """Place the checker in the column"""
    row_index = get_next_available_row(board, col_index)
    if row_index!= -1:
        board[row_index][col_index] = player_checker
        return True
    return False

def check_win(board, player_checker):
    """Check for a win in all directions"""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and \
               board[row][col + 1] == player_checker and \
               board[row][col + 2] == player_checker and \
               board[row][col + 3] == player_checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player_checker and \
               board[row + 1][col] == player_checker and \
               board[row + 2][col] == player_checker and \
               board[row + 3][col] == player_checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and \
               board[row + 1][col + 1] == player_checker and \
               board[row + 2][col + 2] == player_checker and \
               board[row + 3][col + 3] == player_checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and \
               board[row - 1][col + 1] == player_checker and \
               board[row - 2][col + 2] == player_checker and \
               board[row - 3][col + 3] == player_checker:
                return True

    return False

def is_board_full(board):
    """Check if the board is full"""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = players.pop(0)

    while True:
        os.system('clear')
        print_board(board)
        print('Player {}, please enter a column:'.format(get_player_checker(current_player)))
        input_str = input().strip()

        if not is_valid_input(input_str):
            print('Invalid input. Please enter a column letter.')
            continue

        col_index = get_column_index(input_str)
        if is_column_full(board, col_index):
            print('Column is full. Please choose another column.')
            continue

        player_checker = get_player_checker(current_player)
        if place_checker(board, player_checker, col_index):
            if check_win(board, player_checker):
                os.system('clear')
                print_board(board)
                print('Player {} won!'.format(player_checker))
                break

            if is_board_full(board):
                os.system('clear')
                print_board(board)
                print('It\'s a draw!')
                break

            players.append(current_player)
            current_player = players.pop(0)

if __name__ == '__main__':
    main()
