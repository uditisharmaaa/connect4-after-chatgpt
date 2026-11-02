import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """
    Creates a 2D board with specified rows and columns.
    All elements are initialized with whitespaces.
    """
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Prints the current state of the board.
    """
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:COLUMNS]))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def is_valid_input(input_str, columns):
    """
    Checks if the user input is a valid column letter.
    """
    return input_str in string.ascii_uppercase[:columns]

def get_player_checker(player_index):
    """
    Returns the checker symbol for the specified player index.
    """
    return CHECKERS[player_index % len(CHECKERS)]

def place_checker(board, column, checker):
    """
    Places the checker in the specified column.
    If the column is full, returns False.
    """
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return True
    return False

def check_win(board, checker):
    """
    Checks for a win condition (4 in a row) in the board.
    """
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full (draw condition).
    """
    return all([all([cell!= ' ' for cell in row]) for row in board])

def main():
    board = create_board(ROWS, COLUMNS)
    players = [i for i in range(PLAYERS)]
    random.shuffle(players)
    current_player = players[0]
    print_board(board)

    while True:
        checker = get_player_checker(current_player)
        input_str = input(f"Player {checker}, please enter a column: ")
        if not is_valid_input(input_str, COLUMNS):
            print("Invalid input. Please try again.")
            continue
        column = string.ascii_uppercase.index(input_str)
        if not place_checker(board, column, checker):
            print("Column is full. Please try again.")
            continue
        print_board(board)
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
