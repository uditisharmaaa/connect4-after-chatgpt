import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS))
    print(header)
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def get_next_empty_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def check_win(board, player):
    def check_direction(delta_row, delta_col):
        for r in range(ROWS):
            for c in range(COLS):
                if all((0 <= r + i * delta_row < ROWS) and
                       (0 <= c + i * delta_col < COLS) and
                       board[r + i * delta_row][c + i * delta_col] == player for i in range(4)):
                    return True
        return False
    
    return check_direction(1, 0) or check_direction(0, 1) or check_direction(1, 1) or check_direction(1, -1)

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    checkers = CHECKERS[:PLAYERS]
    current_player = random.choice(checkers)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()

        if len(column) != 1 or not column.isalpha() or ord(column) - 65 >= COLS:
            continue

        col_index = ord(column) - 65
        row_index = get_next_empty_row(board, col_index)

        if row_index is None:
            continue

        board[row_index][col_index] = current_player
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("Game is a draw!")
            break
        
        current_player = checkers[(checkers.index(current_player) + 1) % PLAYERS]

main()
