import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_player_count():
    # Set the number of players, ensure it's between MIN_PLAYERS and max available checkers
    return 2

def get_random_starting_player(num_players):
    return random.randint(0, num_players - 1)

def is_valid_move(column, board):
    if column < 0 or column >= COLUMNS or board[0][column] != ' ':
        return False
    return True

def make_move(column, checker, board):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_for_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_valid_column_input():
    while True:
        try:
            column = input('Please enter a column: ').strip().upper()
            if len(column) == 1 and 'A' <= column <= chr(65 + COLUMNS - 1):
                return ord(column) - 65
            else:
                print('Invalid input, try again.')
        except (ValueError, IndexError):
            print('Invalid input, try again.')

def connect_four():
    board = create_board()
    num_players = get_player_count()
    current_player_idx = get_random_starting_player(num_players)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player_idx]
        print(f"Player {current_checker}, it's your turn.")
        
        column = get_valid_column_input()

        if is_valid_move(column, board):
            make_move(column, current_checker, board)
            print_board(board)

            if check_for_win(board, current_checker):
                print(f'Player {current_checker} won!')
                break

            if check_for_draw(board):
                print('The game is a draw!')
                break

            # Switch to next player
            current_player_idx = (current_player_idx + 1) % num_players
        else:
            print('Invalid move, column is full or does not exist. Try again.')

# Start the game
connect_four()
