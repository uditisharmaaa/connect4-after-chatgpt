import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
WIN_CONDITION = 4

# Define checker symbols for different players
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Creates an empty Connect 4 board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(chr(i) for i in range(65, 65 + COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_column(column_input):
    """Validates if the input column is valid."""
    if len(column_input) == 1 and column_input.isalpha():
        column_index = ord(column_input.upper()) - 65
        if 0 <= column_index < COLUMNS:
            return column_index
    return None

def get_first_open_row(board, column):
    """Returns the row index where the checker can be placed in specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            return row
    return None

def place_checker(board, row, column, checker):
    """Places the checker on the board."""
    board[row][column] = checker

def check_winner(board, checker):
    """Checks the board for a win condition with the current checker."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False
    
def check_draw(board):
    """Checks if the board is completely filled and results in a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    num_players = 2  # Setting 2 players for this submission
    board = create_board()
    current_player = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        print(f"Player {PLAYER_CHECKERS[current_player]}, it's your turn.")
        column_input = input("Please enter a column: ").strip()
        column = is_valid_column(column_input)

        if column is not None:
            row = get_first_open_row(board, column)
            if row is not None:
                place_checker(board, row, column, PLAYER_CHECKERS[current_player])
                print_board(board)

                if check_winner(board, PLAYER_CHECKERS[current_player]):
                    print(f"Player {PLAYER_CHECKERS[current_player]} won!")
                    break

                if check_draw(board):
                    print("The game is a draw!")
                    break

                current_player = (current_player + 1) % num_players
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

if __name__ == "__main__":
    main()
