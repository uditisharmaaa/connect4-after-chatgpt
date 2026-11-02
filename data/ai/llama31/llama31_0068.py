import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Creates an empty board with the specified rows and columns."""
    board = []
    for _ in range(rows):
        row = [' ' for _ in range(cols)]
        board.append(row)
    return board

def print_board(board, cols):
    """Prints the board with column labels."""
    print('  ' + ' '.join(string.ascii_uppercase[:cols]))
    print('+---' * cols + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * cols + '+')

def is_valid_input(input_str, cols):
    """Checks if the input is a valid column label."""
    return len(input_str) == 1 and input_str.upper() in string.ascii_uppercase[:cols]

def get_player_input(player, board, cols):
    """Gets the player's input and validates it."""
    while True:
        input_str = input(f"Player {player}, please enter a column: ")
        if is_valid_input(input_str, cols):
            col_idx = string.ascii_uppercase[:cols].index(input_str.upper())
            if ' ' not in board[-1][col_idx]:
                return col_idx
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid input. Please enter a column label (e.g., A).")

def place_checker(board, col_idx, player):
    """Places the player's checker in the specified column."""
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            break

def check_win(board, player):
    """Checks if the player has won."""
    # Check horizontal locations for win
    for row in board:
        for col_idx in range(len(row) - 3):
            if row[col_idx] == player and row[col_idx + 1] == player and row[col_idx + 2] == player and row[col_idx + 3] == player:
                return True

    # Check vertical locations for win
    for col_idx in range(len(board[0])):
        for row_idx in range(len(board) - 3):
            if board[row_idx][col_idx] == player and board[row_idx + 1][col_idx] == player and board[row_idx + 2][col_idx] == player and board[row_idx + 3][col_idx] == player:
                return True

    # Check positively sloped diagonals
    for row_idx in range(len(board) - 3):
        for col_idx in range(len(board[0]) - 3):
            if board[row_idx][col_idx] == player and board[row_idx + 1][col_idx + 1] == player and board[row_idx + 2][col_idx + 2] == player and board[row_idx + 3][col_idx + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row_idx in range(3, len(board)):
        for col_idx in range(len(board[0]) - 3):
            if board[row_idx][col_idx] == player and board[row_idx - 1][col_idx + 1] == player and board[row_idx - 2][col_idx + 2] == player and board[row_idx - 3][col_idx + 3] == player:
                return True

def check_draw(board):
    """Checks if the game is a draw."""
    for row in board:
        for col in row:
            if col == ' ':
                return False
    return True

def play_game(num_players):
    """Plays the game with the specified number of players."""
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    os.system('clear')
    print_board(board, BOARD_COLS)

    while True:
        current_player = players[current_player_idx]
        col_idx = get_player_input(current_player, board, BOARD_COLS)
        place_checker(board, col_idx, current_player)

        os.system('clear')
        print_board(board, BOARD_COLS)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

# Set the number of players and play the game
num_players = 2
play_game(num_players)
