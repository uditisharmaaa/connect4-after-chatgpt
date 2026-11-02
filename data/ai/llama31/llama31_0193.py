import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board with the given dimensions."""
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLUMNS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board, player_turn):
    """Print the current state of the game board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    print('+---+---+---+---+---+---+---+')
    for row in board:
        row_str = '|'
        for cell in row:
            row_str += ' ' + cell + ' |'
        print(row_str)
        print('+---+---+---+---+---+---+---+')
    print('Player', CHECKERS[player_turn], ', please enter a column:')

def is_valid_input(column):
    """Check if the user's input is a valid column."""
    if len(column)!= 1:
        return False
    if not column.isalpha():
        return False
    if not 'A' <= column <= 'G':
        return False
    return True

def get_column_from_input(input_str):
    """Get the column number from the user's input."""
    return ord(input_str.upper()) - ord('A')

def is_column_full(board, column):
    """Check if the column is already full."""
    return board[0][column]!= ' '

def place_checker(board, column, checker):
    """Place the checker in the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_COLUMNS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
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
        print_board(board, current_player)
        column_input = input()
        if not is_valid_input(column_input):
            print('Invalid input. Please enter a letter from A to G.')
            input('Press enter to continue...')
            continue
        column = get_column_from_input(column_input)
        if is_column_full(board, column):
            print('Column is full. Please choose another column.')
            input('Press enter to continue...')
            continue
        place_checker(board, column, CHECKERS[current_player])
        if check_win(board, CHECKERS[current_player]):
            print_board(board, current_player)
            print('Player', CHECKERS[current_player], 'won!')
            break
        if check_draw(board):
            print_board(board, current_player)
            print('It\'s a draw!')
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
