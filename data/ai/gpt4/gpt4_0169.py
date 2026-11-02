import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Maximum of 5 players
MAX_PLAYERS = 5

def create_board():
    """Creates an empty game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_column(column, board):
    """Checks if the selected column is valid and not full."""
    return 0 <= column < COLUMNS and board[0][column] == ' '

def get_column_input(board):
    """Gets and validates user input for the column."""
    while True:
        try:
            column_input = input("Please enter a column: ").strip().upper()
            if len(column_input) != 1 or not column_input.isalpha():
                raise ValueError
            column = ord(column_input) - 65
            if is_valid_column(column, board):
                return column
            else:
                print("Invalid column. Please try again.")
        except ValueError:
            print("Invalid input. Enter a valid column letter from A to {}".format(chr(64 + COLUMNS)))

def drop_checker(board, column, checker):
    """Drops the checker into the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_winner(board, checker):
    """Checks if a player has won with 4 in a row."""
    # Horizontal check
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw (no empty spaces left)."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    # Initialize game
    board = create_board()
    player_count = PLAYERS  # You can adjust this for more players (up to MAX_PLAYERS)
    checkers_in_game = CHECKERS[:player_count]
    current_player = random.randint(0, player_count - 1)

    # Print the initial board
    print_board(board)
    print("Player {} starts!".format(checkers_in_game[current_player]))

    while True:
        # Current player turn
        print("Player {}'s turn.".format(checkers_in_game[current_player]))
        column = get_column_input(board)
        drop_checker(board, column, checkers_in_game[current_player])
        print_board(board)

        # Check for win or draw
        if check_winner(board, checkers_in_game[current_player]):
            print("Player {} won!".format(checkers_in_game[current_player]))
            break
        elif is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % player_count

if __name__ == "__main__":
    main()
