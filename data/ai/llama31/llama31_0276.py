import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create a 2D list filled with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board."""
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('|   ' * BOARD_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('|   ' * BOARD_COLS + '|')
        print('+---' * BOARD_COLS + '+')

def is_valid_input(column, board):
    """Check if the user input is valid."""
    try:
        column = string.ascii_uppercase.index(column.upper())
        return 0 <= column < BOARD_COLS and board[0][column] == ' '
    except ValueError:
        return False

def get_player_input(player, board):
    """Get the user input and validate it."""
    while True:
        column = input(f"Player {player}, please enter a column: ")
        if is_valid_input(column, board):
            return string.ascii_uppercase.index(column.upper())
        else:
            print("Invalid input. Please enter a letter from A to G.")

def drop_checker(column, player, board):
    """Drop the checker into the selected column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            break

def check_win(player, board):
    """Check if the current player has won."""
    # Check horizontal locations for win
    for row in board:
        for col in range(BOARD_COLS - 3):
            if row[col] == player and row[col + 1] == player and row[col + 2] == player and row[col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Start the Connect 4 game."""
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board)
        column = get_player_input(current_player, board)
        drop_checker(column, current_player, board)
        if check_win(current_player, board):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    game()
