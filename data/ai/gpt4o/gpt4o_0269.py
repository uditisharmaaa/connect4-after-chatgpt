import os
import random

# Constants
ROWS, COLS = 6, 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def init_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = ' '.join([chr(65 + i) for i in range(len(board[0]))])
    print('  ' + '   '.join(col_labels))
    for row in board:
        print('+---' * len(row) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * len(board[0]) + '+')

def is_valid_input(column, board):
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < len(board[0])

def is_column_full(column, board):
    col_index = ord(column.upper()) - 65
    return all(row[col_index] != ' ' for row in board)

def place_checker(column, board, symbol):
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = symbol
            return

def check_winner(board, symbol):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if (check_horizontal(row, col, board, symbol) or 
                check_vertical(row, col, board, symbol) or 
                check_diagonal(row, col, board, symbol)):
                return True
    return False

def check_horizontal(row, col, board, symbol):
    return col + 3 < len(board[0]) and all(board[row][col + i] == symbol for i in range(4))

def check_vertical(row, col, board, symbol):
    return row + 3 < len(board) and all(board[row + i][col] == symbol for i in range(4))

def check_diagonal(row, col, board, symbol):
    return (col + 3 < len(board[0]) and row + 3 < len(board) and 
            all(board[row + i][col + i] == symbol for i in range(4)) or
            col - 3 >= 0 and row + 3 < len(board) and 
            all(board[row + i][col - i] == symbol for i in range(4)))

def is_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def connect_4():
    board = init_board(ROWS, COLS)
    current_player = random.randint(0, 1)
    players = PLAYER_SYMBOLS[:2]

    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn. Please enter a column:")
        while True:
            column = input().strip()
            if is_valid_input(column, board) and not is_column_full(column, board):
                break
            print("Invalid input. Try again:")

        place_checker(column, board, players[current_player])
        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % len(players)

if __name__ == '__main__':
    connect_4()
