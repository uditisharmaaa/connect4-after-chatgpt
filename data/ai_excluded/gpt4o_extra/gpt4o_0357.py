import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    """Initialize and return the game board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def check_win(board, checker):
    """Check if the current checker has won the game."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (check_sequence(board, checker, row, col, 0, 1) or
                check_sequence(board, checker, row, col, 1, 0) or
                check_sequence(board, checker, row, col, 1, 1) or
                check_sequence(board, checker, row, col, 1, -1)):
                return True
    return False

def check_sequence(board, checker, row, col, delta_row, delta_col):
    """Check if there is a sequence of four checkers starting at (row, col)."""
    for i in range(4):
        if not (0 <= row+i*delta_row < ROWS and 0 <= col+i*delta_col < COLUMNS):
            return False
        if board[row+i*delta_row][col+i*delta_col] != checker:
            return False
    return True

def check_draw(board):
    """Check if the board is full, hence the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def place_checker(board, col, checker):
    """Place the checker in the specified column if possible."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def valid_input(input_char):
    """Validate user input for column selection."""
    return input_char.isalpha() and 'A' <= input_char <= chr(65 + COLUMNS - 1)

def play_game():
    """Main function to play the game."""
    board = initialize_board(ROWS, COLUMNS)
    current_turn = random.randint(0, MAX_PLAYERS - 1)
    players = [CHECKERS[i] for i in range(MAX_PLAYERS)]

    print_board(board)
    while True:
        player_checker = players[current_turn]
        print(f"Player {player_checker}, please enter a column:")
        move = input().strip().upper()

        if not valid_input(move):
            print("Invalid input. Please try again.")
            continue

        column = ord(move) - 65

        if not place_checker(board, column, player_checker):
            print("Column is full. You lose your turn.")
        else:
            print_board(board)
            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

        current_turn = (current_turn + 1) % MAX_PLAYERS

play_game()
