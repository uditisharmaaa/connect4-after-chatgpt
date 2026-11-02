import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """Create an empty board with the given dimensions."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def get_player_checker(player_number):
    """Get the checker symbol for the given player number."""
    return CHECKERS[player_number - 1]

def get_next_player(current_player):
    """Get the next player number."""
    return (current_player % PLAYERS) + 1

def is_valid_input(input_str):
    """Check if the input is a valid column letter."""
    return input_str.upper().isalpha() and ord(input_str.upper()) - 64 <= COLUMNS

def get_column_from_input(input_str):
    """Get the column number from the input letter."""
    return ord(input_str.upper()) - 65

def place_checker(board, column, checker):
    """Place the checker in the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal wins
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == checker:
                return True

    # Check vertical wins
    for column in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][column] == board[i + 1][column] == board[i + 2][column] == board[i + 3][column] == checker:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if board[row][column] == board[row + 1][column + 1] == board[row + 2][column + 2] == board[row + 3][column + 3] == checker:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for column in range(COLUMNS - 3):
            if board[row][column] == board[row - 1][column + 1] == board[row - 2][column + 2] == board[row - 3][column + 3] == checker:
                return True

    return False

def check_draw(board):
    """Check if the board is full."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(1, PLAYERS)

    while True:
        print_board(board)
        print("Player", current_player, "(", get_player_checker(current_player), ")")

        while True:
            input_str = input("Please enter a column (A-{}): ".format(chr(65 + COLUMNS - 1)))
            if is_valid_input(input_str):
                column = get_column_from_input(input_str)
                if board[0][column]!= ' ':
                    print("Column is full, please choose another column.")
                else:
                    break
            else:
                print("Invalid input, please try again.")

        place_checker(board, column, get_player_checker(current_player))

        if check_win(board, get_player_checker(current_player)):
            print_board(board)
            print("Player", current_player, "won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = get_next_player(current_player)

if __name__ == "__main__":
    main()
