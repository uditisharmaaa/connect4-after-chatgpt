import os
import random

ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = ' '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print('  ' + col_labels)
    for row in board:
        print('+---' * len(row) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * len(board[0]) + '+')

def check_valid_column(board, column):
    return column.isalpha() and ord(column) - ord('A') < len(board[0]) and board[0][ord(column) - ord('A')] == ' '

def drop_checker(board, column, checker):
    for i in range(len(board) - 1, -1, -1):
        if board[i][ord(column) - ord('A')] == ' ':
            board[i][ord(column) - ord('A')] = checker
            return i, ord(column) - ord('A')

def has_won(board, row, col, checker):
    def check_direction(dx, dy):
        count = 0
        x, y = row, col
        while 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == checker:
            count += 1
            x, y = x + dx, y + dy
        return count >= 4

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        if check_direction(dx, dy) + check_direction(-dx, -dy) - 1 >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def play_game():
    players = ['X', 'O', 'V', 'H', 'M']
    num_players = 2
    checkers = players[:num_players]
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.choice(range(num_players))
    
    print_board(board)
    
    while True:
        player = checkers[current_player_index]
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        
        if not check_valid_column(board, column):
            print("Invalid input. Try again.")
            continue

        row, col = drop_checker(board, column, player)
        print_board(board)

        if has_won(board, row, col, player):
            print(f"Player {player} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

play_game()
