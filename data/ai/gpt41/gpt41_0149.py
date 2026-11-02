import os
import random
import string

# ---- Constants ---- #
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Support 2-5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    header = '  ' + '   '.join(COLUMN_LABELS)
    print(header)
    print('+' + '---+'*COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+'*COLUMNS)

def get_player_checker(player_idx):
    return CHECKERS[player_idx]

def input_column(board, player_checker):
    while True:
        move = input(f'Player {player_checker}, please enter a column: ').strip().upper()
        if len(move) != 1 or move not in COLUMN_LABELS:
            print('Invalid input. Enter a valid column letter.')
            continue
        col = COLUMN_LABELS.index(move)
        if board[0][col] != ' ':
            print('Column is full. Turn lost.')
            return None  # Lose turn
        return col

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_winner(board, last_row, last_col, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr,dc in directions:
        count = 1
        for d in [1,-1]:
            r, c = last_row, last_col
            while True:
                r += dr*d
                c += dc*d
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    player = random.randrange(PLAYERS)
    print_board(board)
    while True:
        checker = get_player_checker(player)
        col = input_column(board, checker)
        if col is None:
            player = (player + 1) % PLAYERS
            continue
        row, col = place_checker(board, col, checker)
        print_board(board)
        if check_winner(board, row, col, checker):
            print(f'Player {checker} won!')
            break
        if board_full(board):
            print('It\'s a draw!')
            break
        player = (player + 1) % PLAYERS

if __name__ == "__main__":
    main()
