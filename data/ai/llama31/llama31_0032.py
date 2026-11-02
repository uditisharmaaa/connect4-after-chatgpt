import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with the specified dimensions."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player):
    """Get the checker for the specified player."""
    return CHECKERS[player]

def is_valid_move(board, col):
    """Check if the move is valid (i.e., the column is not full)."""
    return board[0][col] == ' '

def make_move(board, player, col):
    """Make a move for the specified player in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = get_player_checker(player)
            break

def check_win(board, player):
    """Check if the specified player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i+1] == row[i+2] == row[i+3] == get_player_checker(player):
                return True

    # Check vertical wins
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == get_player_checker(player):
                return True

    # Check diagonal wins
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == get_player_checker(player):
                return True
            if board[row][col+3] == board[row+1][col+2] == board[row+2][col+1] == board[row+3][col] == get_player_checker(player):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw (i.e., the board is full)."""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the game."""
    board = create_board()
    players = list(range(NUM_PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        player = players[current_player]
        checker = get_player_checker(player)
        print(f"Player {checker}, please enter a column (A-{chr(ord('A') + NUM_COLS - 1)}):")

        while True:
            col = input().strip().upper()
            if col < 'A' or col > chr(ord('A') + NUM_COLS - 1):
                print("Invalid input. Please enter a valid column.")
            elif not is_valid_move(board, ord(col) - ord('A')):
                print("Invalid input. The column is already full.")
            else:
                break

        make_move(board, player, ord(col) - ord('A'))

        if check_win(board, player):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

game()
