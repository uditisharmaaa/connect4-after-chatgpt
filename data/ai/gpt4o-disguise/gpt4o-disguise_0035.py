import os
import random

# Global constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Use only needed checkers

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
    print('+' + '---+' * COLS)

def player_won(board, symbol):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if check_line(board, row, col, symbol):
                return True
    return False

def check_line(board, row, col, symbol):
    return check_direction(board, row, col, symbol, 1, 0) or check_direction(board, row, col, symbol, 0, 1) or check_direction(board, row, col, symbol, 1, 1) or check_direction(board, row, col, symbol, 1, -1)

def check_direction(board, row, col, symbol, row_step, col_step):
    try:
        for i in range(4):
            if board[row + row_step * i][col + col_step * i] != symbol:
                return False
        return True
    except IndexError:
        return False

def board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def game():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        player_symbol = CHECKERS[current_player]
        column = input(f"Player {player_symbol}, please enter a column: ").strip().upper()

        if len(column) != 1 or not ('A' <= column <= chr(ord('A') + COLS - 1)):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_idx = ord(column) - ord('A')

        if board[0][col_idx] != ' ':
            print("Column full. You've lost your turn.")
            current_player = (current_player + 1) % PLAYERS
            continue

        for row in reversed(range(ROWS)):
            if board[row][col_idx] == ' ':
                board[row][col_idx] = player_symbol
                break

        print_board(board)

        if player_won(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

game()
