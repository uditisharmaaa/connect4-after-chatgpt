import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with specified dimensions."""
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

def is_valid_input(board, column):
    """Check if the input column is valid."""
    try:
        column = ord(column) - 65
        if column < 0 or column >= COLUMNS:
            return False
        return board[0][column] == ' '
    except ValueError:
        return False

def get_player_input(player):
    """Get a valid input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if is_valid_input(board, column):
            return column
        print("Invalid input. Please try again.")

def place_checker(board, player, column):
    """Place the checker in the specified column."""
    column = ord(column) - 65
    for i in range(ROWS - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = player
            break

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Create the board and randomly select the first player
board = create_board()
current_player = random.randint(0, PLAYERS - 1)

# Game loop
while True:
    print_board(board)
    player = CHECKERS[current_player]
    column = get_player_input(player)
    place_checker(board, player, column)
    if check_win(board, player):
        print_board(board)
        print(f"Player {player} won!")
        break
    elif check_draw(board):
        print_board(board)
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
