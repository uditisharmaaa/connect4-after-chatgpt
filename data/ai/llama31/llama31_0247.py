import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D list representing the game board."""
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    return board

def print_board(board):
    """Print the game board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(NUM_COLS)))
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|   ' * NUM_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('|   ' * NUM_COLS + '|')
    print('+---' * NUM_COLS + '+')

def get_player_checker(player_index):
    """Get the checker symbol for a player."""
    return CHECKERS[player_index]

def is_valid_move(board, col):
    """Check if a move is valid."""
    return board[NUM_ROWS - 1][col] == ' '

def make_move(board, col, checker):
    """Make a move on the board."""
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return

def check_win(board, checker):
    """Check if a player has won."""
    # Check horizontal locations for win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col]!= ' ' for col in range(NUM_COLS))

def game():
    """Play the Connect 4 game."""
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player_index = 0

    while True:
        print_board(board)
        current_player = players[current_player_index]
        checker = get_player_checker(current_player)
        print(f"Player {checker}, please enter a column (A-{chr(64 + NUM_COLS)}):")
        col = input().strip().upper()

        if not col.isalpha() or not 'A' <= col <= chr(64 + NUM_COLS):
            print("Invalid input. Please try again.")
            continue

        col = ord(col) - 65
        if not is_valid_move(board, col):
            print("Column is full. Please try again.")
            continue

        make_move(board, col, checker)
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

game()
