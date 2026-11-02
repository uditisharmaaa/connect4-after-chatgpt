import random
import os

# Constants to set the number of players
PLAYER_COUNT = 2  # Change this value between 2 and 5

# Player symbols
SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

# Board dimensions
ROWS, COLUMNS = 6, 7
COLUMN_LABELS = 'ABCDEFG'

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')

def make_move(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return True
    return False

def is_valid_move(board, column):
    return board[0][column] == ' '

def check_winner(board, symbol):
    def check_direction(r, c, dr, dc):
        return all(0 <= r + i*dr < ROWS and 0 <= c + i*dc < COLUMNS and board[r + i*dr][c + i*dc] == symbol for i in range(4))
    
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (check_direction(r, c, 1, 0) or  # Vertical
                check_direction(r, c, 0, 1) or  # Horizontal
                check_direction(r, c, 1, 1) or  # Diagonal down-right
                check_direction(r, c, 1, -1)):  # Diagonal down-left
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def get_player_move():
    while True:
        move = input(f"Enter column (A-{COLUMN_LABELS[COLUMNS-1]}): ").strip().upper()
        if move in COLUMN_LABELS and is_valid_move(board, COLUMN_LABELS.index(move)):
            return COLUMN_LABELS.index(move)
        print("Invalid move. Try again.")

def play_game():
    board = create_board()
    current_player = random.choice(SYMBOLS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")
        col = get_player_move()

        if make_move(board, col, current_player):
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player = SYMBOLS[(SYMBOLS.index(current_player) + 1) % PLAYER_COUNT]

if __name__ == '__main__':
    play_game()
