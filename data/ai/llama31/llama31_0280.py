import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

# Checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the given dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print(' ' + ' '.join(string.ascii_uppercase[:COLS]))
    print('+---' * COLS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLS + '+')

def get_player_checker(player):
    """Get the checker for the given player."""
    return CHECKERS[player % len(CHECKERS)]

def drop_checker(board, col, checker):
    """Drop a checker in the given column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    """Check if the given player has won."""
    # Check horizontal wins
    for row in board:
        for i in range(COLS - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True

    # Check vertical wins
    for col in range(COLS):
        for i in range(ROWS - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all([cell!= ' ' for row in board for cell in row])

def game():
    """Play the Connect 4 game."""
    board = create_board()
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = 0

    while True:
        print_board(board)
        player = players[current_player]
        checker = get_player_checker(player)
        print(f"Player {checker}, please enter a column:")

        while True:
            col = input().strip().upper()
            if col not in string.ascii_uppercase[:COLS]:
                print("Invalid column. Please try again.")
            elif board[0][string.ascii_uppercase.index(col)]!= ' ':
                print("Column is full. Please try again.")
            else:
                col = string.ascii_uppercase.index(col)
                drop_checker(board, col, checker)
                break

        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    game()
