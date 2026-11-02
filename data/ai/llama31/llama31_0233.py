import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board."""
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_number):
    """Get the checker for the given player."""
    return CHECKERS[player_number]

def get_next_player(current_player):
    """Get the next player."""
    return (current_player + 1) % PLAYERS

def get_column_from_input(player_input):
    """Get the column index from the player's input."""
    return ord(player_input.upper()) - ord('A')

def is_valid_input(player_input):
    """Check if the player's input is valid."""
    return 'A' <= player_input.upper() <= 'G'

def is_column_full(board, column_index):
    """Check if the column is full."""
    return board[0][column_index]!= ' '

def get_next_available_row(board, column_index):
    """Get the next available row in the column."""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][column_index] == ' ':
            return row_index

def place_checker(board, player_checker, column_index):
    """Place the checker in the column."""
    row_index = get_next_available_row(board, column_index)
    board[row_index][column_index] = player_checker

def check_win(board, player_checker):
    """Check if the player has won."""
    # Check horizontal
    for row in board:
        for i in range(BOARD_COLS - 3):
            if row[i] == player_checker and row[i + 1] == player_checker and row[i + 2] == player_checker and row[i + 3] == player_checker:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(BOARD_ROWS - 3):
            if board[i][col] == player_checker and board[i + 1][col] == player_checker and board[i + 2][col] == player_checker and board[i + 3][col] == player_checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row + 1][col + 1] == player_checker and board[row + 2][col + 2] == player_checker and board[row + 3][col + 3] == player_checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player_checker and board[row - 1][col + 1] == player_checker and board[row - 2][col + 2] == player_checker and board[row - 3][col + 3] == player_checker:
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board)
        player_checker = get_player_checker(current_player)
        print('Player', player_checker, ', please enter a column:')

        while True:
            player_input = input().strip()
            if is_valid_input(player_input):
                column_index = get_column_from_input(player_input)
                if not is_column_full(board, column_index):
                    break
                else:
                    print('Column is full. Please choose another column.')
            else:
                print('Invalid input. Please enter a letter between A and G.')

        place_checker(board, player_checker, column_index)

        if check_win(board, player_checker):
            os.system('clear')
            print_board(board)
            print('Player', player_checker, 'won!')
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print('It\'s a draw!')
            break

        current_player = get_next_player(current_player)

if __name__ == '__main__':
    main()
