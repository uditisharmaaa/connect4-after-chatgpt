import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board, players):
    os.system('clear')
    print(' '.join(string.ascii_uppercase[:BOARD_COLS]))
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('| {} |'.format(' | '.join(row)))
        print('+---' * BOARD_COLS + '+')
    print('Player {}, please enter a column:'.format(players[0]))

def is_valid_input(col, board):
    return col in string.ascii_uppercase[:BOARD_COLS] and board[0][string.ascii_uppercase.index(col)] == ' '

def get_next_player(players):
    return players[1:] + [players[0]]

def drop_checker(board, col, player):
    for row in reversed(board):
        if row[string.ascii_uppercase.index(col)] == ' ':
            row[string.ascii_uppercase.index(col)] = player
            return

def check_win(board, player):
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

def check_draw(board):
    return ' ' not in [cell for row in board for cell in row]

def game():
    players = CHECKERS[:2]  # 2 players enabled
    random.shuffle(players)
    board = create_board()
    while True:
        print_board(board, players)
        col = input().upper()
        if not is_valid_input(col, board):
            print('Invalid input, please try again.')
            continue
        drop_checker(board, col, players[0])
        if check_win(board, players[0]):
            print_board(board, players)
            print('Player {} won!'.format(players[0]))
            break
        elif check_draw(board):
            print_board(board, players)
            print('It\'s a draw!')
            break
        players = get_next_player(players)

if __name__ == '__main__':
    game()
