import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """
    Create a 2D board with whitespaces
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """
    Print the board with column labels
    """
    print(' ' + '   '.join([chr(65 + i) for i in range(cols)]))
    print('+---' * cols + '+')
    for row in board:
        print('|   ' * cols + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('|   ' * cols + '|')
        print('+---' * cols + '+')

def get_player_checker(player_num):
    """
    Get the checker for a player
    """
    return CHECKERS[player_num - 1]

def get_column_label(col):
    """
    Get the column label from a column index
    """
    return chr(65 + col)

def validate_input(input_str, cols):
    """
    Validate user input
    """
    if len(input_str)!= 1 or not input_str.isalpha():
        return False
    col = ord(input_str.upper()) - 65
    return 0 <= col < cols

def get_valid_input(player_checker, cols):
    """
    Get valid input from user
    """
    while True:
        input_str = input(f"Player {player_checker}, please enter a column: ")
        if validate_input(input_str, cols):
            return ord(input_str.upper()) - 65

def place_checker(board, col, player_checker):
    """
    Place a checker in a column
    """
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player_checker
            return

def check_win(board, player_checker):
    """
    Check for a win in all directions
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for row in board:
        for col in range(cols - 3):
            if row[col] == player_checker and row[col + 1] == player_checker and row[col + 2] == player_checker and row[col + 3] == player_checker:
                return True

    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if board[row][col] == player_checker and board[row + 1][col] == player_checker and board[row + 2][col] == player_checker and board[row + 3][col] == player_checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == player_checker and board[row + 1][col + 1] == player_checker and board[row + 2][col + 2] == player_checker and board[row + 3][col + 3] == player_checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if board[row][col] == player_checker and board[row - 1][col + 1] == player_checker and board[row - 2][col + 2] == player_checker and board[row - 3][col + 3] == player_checker:
                return True

    return False

def check_draw(board):
    """
    Check if the board is full
    """
    return all(all(cell!= ' ' for cell in row) for row in board)

def game():
    """
    Main game loop
    """
    board = create_board(BOARD_ROWS, BOARD_COLS)
    num_players = 2
    players = [get_player_checker(i) for i in range(1, num_players + 1)]
    current_player = random.choice(players)

    os.system('clear')
    print_board(board, BOARD_COLS)

    while True:
        col = get_valid_input(current_player, BOARD_COLS)
        place_checker(board, col, current_player)

        os.system('clear')
        print_board(board, BOARD_COLS)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % num_players]

game()
