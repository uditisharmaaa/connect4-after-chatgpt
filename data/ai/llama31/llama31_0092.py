import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the specified dimensions"""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players, current_player):
    """Print the current state of the board"""
    os.system('clear')
    print(' ' + ' '.join(string.ascii_uppercase[:BOARD_COLS]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')
    print(f'Player {players[current_player - 1]}, please enter a column: ')

def get_player_move():
    """Get the player's move and validate it"""
    while True:
        move = input().upper()
        if move in string.ascii_uppercase[:BOARD_COLS]:
            return string.ascii_uppercase.index(move)
        print('Invalid input. Please enter a column letter.')

def place_checker(board, column, checker):
    """Place a checker in the specified column"""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return
    print('Column is full. Please choose another column.')

def check_win(board, checker):
    """Check for a win in the current state of the board"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True
    return False

def check_draw(board):
    """Check for a draw (board is full and no player has won)"""
    return all([cell!= ' ' for row in board for cell in row])

def main():
    board = create_board()
    players = CHECKERS[:2]  # Default to 2 players
    current_player = random.randint(0, len(players) - 1)
    while True:
        print_board(board, players, current_player + 1)
        column = get_player_move()
        place_checker(board, column, players[current_player])
        if check_win(board, players[current_player]):
            print_board(board, players, current_player + 1)
            print(f'Player {players[current_player]} won!')
            break
        elif check_draw(board):
            print_board(board, players, current_player + 1)
            print('It\'s a draw!')
            break
        current_player = (current_player + 1) % len(players)

if __name__ == '__main__':
    main()
