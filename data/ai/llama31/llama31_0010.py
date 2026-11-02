import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    print('  A', end='')
    for col in range(1, BOARD_COLS):
        print(f'  {chr(ord("A") + col)}', end='')
    print()
    print('+---' * BOARD_COLS + '+')
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            print(f'| {board[row][col]} ', end='')
        print('|')
        print('+---' * BOARD_COLS + '+')

def get_player_checker(player_index):
    """Get the checker for the specified player."""
    return CHECKERS[player_index]

def is_valid_input(col):
    """Check if the input column is valid."""
    return 'A' <= col <= chr(ord("A") + BOARD_COLS - 1)

def get_column_index(col):
    """Convert the input column to an index."""
    return ord(col) - ord("A")

def is_column_full(board, col_index):
    """Check if the specified column is full."""
    return board[0][col_index]!= ' '

def place_checker(board, col_index, checker):
    """Place the checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all(all(cell!= ' ' for cell in row) for row in board)

def game():
    board = create_board()
    num_players = 2  # Set to 2 for submission
    players = list(range(num_players))
    random.shuffle(players)  # Randomly select the first player
    current_player_index = 0

    while True:
        os.system('clear')
        print_board(board)
        player_checker = get_player_checker(players[current_player_index])
        print(f"Player {player_checker}, please enter a column:")

        while True:
            col = input().upper()
            if is_valid_input(col):
                col_index = get_column_index(col)
                if not is_column_full(board, col_index):
                    place_checker(board, col_index, player_checker)
                    break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a letter between A and", chr(ord("A") + BOARD_COLS - 1))

        if check_win(board, player_checker):
            os.system('clear')
            print_board(board)
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    game()
