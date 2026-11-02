import os
import random

# Constant global variables
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D board with whitespaces"""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')
    print()

def get_player_checker(player):
    """Get the checker for a given player"""
    return CHECKERS[player - 1]

def is_valid_move(board, column):
    """Check if a move is valid"""
    return board[0][column] == ' '

def make_move(board, player, column):
    """Make a move on the board"""
    checker = get_player_checker(player)
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, player):
    """Check for a win on the board"""
    checker = get_player_checker(player)
    # Check horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True
    # Check vertical
    for column in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][column] == checker and board[i+1][column] == checker and board[i+2][column] == checker and board[i+3][column] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if board[row][column] == checker and board[row+1][column+1] == checker and board[row+2][column+2] == checker and board[row+3][column+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for column in range(COLUMNS - 3):
            if board[row][column] == checker and board[row-1][column+1] == checker and board[row-2][column+2] == checker and board[row-3][column+3] == checker:
                return True
    return False

def check_draw(board):
    """Check for a draw on the board"""
    return all(cell!= ' ' for row in board for cell in row)

def game():
    """Play the Connect 4 game"""
    board = create_board()
    player = random.randint(1, PLAYERS)
    while True:
        print_board(board)
        print(f"Player {get_player_checker(player)}, please enter a column:")
        while True:
            column = input().upper()
            if column in 'ABCDEFG':
                column = ord(column) - ord('A')
                if is_valid_move(board, column):
                    make_move(board, player, column)
                    break
                else:
                    print("Invalid move, column is full. Try again.")
            else:
                print("Invalid input. Please enter a letter between A and G.")
        if check_win(board, player):
            print_board(board)
            print(f"Player {get_player_checker(player)} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        player = (player % PLAYERS) + 1

if __name__ == "__main__":
    game()
