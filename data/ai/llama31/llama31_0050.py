import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    """Create a 2D list representing the game board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    print('  ' + ' '.join(string.ascii_uppercase[:COLUMNS]))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| {} |'.format(' | '.join(row)))
    print('+---' * COLUMNS + '+')

def is_valid_input(input_str):
    """Check if the input is a valid column letter."""
    return input_str.upper() in string.ascii_uppercase[:COLUMNS]

def get_player_checker(player):
    """Get the checker for the given player."""
    return CHECKERS[player]

def place_checker(board, column, checker):
    """Place a checker in the given column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_win(board, checker):
    """Check if the given checker has won."""
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

def is_draw(board):
    """Check if the game is a draw."""
    return all([all([cell!= ' ' for cell in row]) for row in board])

def main():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    players = list(range(PLAYERS))
    current_player = random.choice(players)

    while True:
        # Clear the screen and print the current state of the board
        os.system('clear')
        print_board(board)

        # Get the input from the current player
        input_str = input("Player {}, please enter a column: ".format(get_player_checker(current_player)))
        if not is_valid_input(input_str):
            print("Invalid input. Please try again.")
            continue

        # Place the checker in the given column
        column = string.ascii_uppercase.index(input_str.upper())
        place_checker(board, column, get_player_checker(current_player))

        # Check if the current player has won
        if check_win(board, get_player_checker(current_player)):
            os.system('clear')
            print_board(board)
            print("Player {} won!".format(get_player_checker(current_player)))
            break

        # Check if the game is a draw
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
