import os
import random

ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
players = CHECKERS[:MAX_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLUMNS)]))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')
    
def make_move(board, player, column):
    col_index = ord(column.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return True
    return False

def check_win(board, player):
    for r in range(ROWS):
        for c in range(COLUMNS):
            if all(board[r+i][c] == player for i in range(4) if r + i < ROWS) or \
               all(board[r][c+i] == player for i in range(4) if c + i < COLUMNS) or \
               all(board[r+i][c+i] == player for i in range(4) if r + i < ROWS and c + i < COLUMNS) or \
               all(board[r+i][c-i] == player for i in range(4) if r + i < ROWS and c - i >= 0):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, MAX_PLAYERS - 1)
    print_board(board)
    
    while True:
        player = players[current_player_index]
        column = input(f"Player {player}, please enter a column: ").strip()
        if len(column) == 1 and 'A' <= column <= chr(ord('A') + COLUMNS - 1):
            if make_move(board, player, column):
                print_board(board)
                if check_win(board, player):
                    print(f"Player {player} won!")
                    break
                if check_draw(board):
                    print("The game is a draw!")
                    break
                current_player_index = (current_player_index + 1) % MAX_PLAYERS
            else:
                print("Column is full, turn lost.")
        else:
            print("Invalid input, try again.")

play_game()
