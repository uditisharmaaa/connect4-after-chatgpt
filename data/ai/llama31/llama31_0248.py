import os
import random
import string

# Constant global variables
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with given dimensions"""
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:COLUMNS]))
    print('+---' + '+---' * (COLUMNS - 1))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' + '+---' * (COLUMNS - 1))

def get_player_checker(player_number):
    """Get the checker for a given player number"""
    return CHECKERS[player_number - 1]

def is_valid_input(column):
    """Check if the input is a valid column letter"""
    return column in string.ascii_uppercase[:COLUMNS]

def is_valid_move(board, column):
    """Check if a move is valid (column is not full)"""
    return board[0][string.ascii_uppercase.index(column)] == ' '

def get_next_open_row(board, column):
    """Get the next open row in a given column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][string.ascii_uppercase.index(column)] == ' ':
            return row

def make_move(board, player_number, column):
    """Make a move on the board"""
    row = get_next_open_row(board, column)
    board[row][string.ascii_uppercase.index(column)] = get_player_checker(player_number)

def check_win(board, player_number):
    """Check if a player has won"""
    checker = get_player_checker(player_number)
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True
    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw(board):
    """Check if the game is a draw"""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    # Create the board
    board = create_board()
    # Randomly select the first player
    current_player = random.randint(1, PLAYERS)
    while True:
        # Print the current state of the board
        print_board(board)
        # Get the column from the current player
        column = input(f"Player {get_player_checker(current_player)}, please enter a column: ").upper()
        # Validate the input
        while not is_valid_input(column) or not is_valid_move(board, column):
            column = input("Invalid input, please try again: ").upper()
        # Make the move
        make_move(board, current_player, column)
        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {get_player_checker(current_player)} won!")
            break
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        # Switch to the next player
        current_player = (current_player % PLAYERS) + 1

if __name__ == "__main__":
    main()
