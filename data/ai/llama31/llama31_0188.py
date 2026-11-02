import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players):
    """Print the current state of the board."""
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')
    print(f"Player {players[0]}, please enter a column:")

def validate_input(column):
    """Check if the input is a valid column letter."""
    if column not in string.ascii_uppercase[:BOARD_COLS]:
        return False
    return True

def get_player_move(players):
    """Get the move from the current player."""
    while True:
        column = input().upper()
        if validate_input(column):
            return column
        print("Invalid input. Please enter a column letter.")

def drop_checker(board, column, player):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[string.ascii_uppercase.index(column)] == ' ':
            row[string.ascii_uppercase.index(column)] = player
            return

def check_win(board, player):
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

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def game():
    """Play the Connect 4 game."""
    board = create_board()
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    while True:
        print_board(board, players)
        column = get_player_move(players)
        drop_checker(board, column, current_player)
        if check_win(board, current_player):
            print_board(board, players)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print_board(board, players)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    game()
