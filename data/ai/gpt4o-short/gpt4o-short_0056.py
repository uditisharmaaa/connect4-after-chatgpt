import random
import os

# Constants for game configuration
NUMBER_OF_PLAYERS = 3  # You can set this between 2 to 5
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M'][:NUMBER_OF_PLAYERS]

# Game board dimensions
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '-' * (2 * COLUMNS + 1) + '+')

def is_valid_column(column):
    return column in COLUMN_LABELS

def is_column_full(board, column_index):
    return board[0][column_index] != ' '

def drop_piece(board, column_index, piece):
    for row in reversed(range(ROWS)):
        if board[row][column_index] == ' ':
            board[row][column_index] = piece
            return row, column_index

def is_winning_move(board, piece, row, column):
    # Check horizontal
    for c in range(COLUMNS - 3):
        if all(board[row][c+i] == piece for i in range(4)):
            return True

    # Check vertical
    if row <= ROWS - 4:
        if all(board[row+i][column] == piece for i in range(4)):
            return True

    # Check positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negative diagonal
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def play_game():
    board = create_board()
    players = PLAYER_MARKERS[:NUMBER_OF_PLAYERS]
    current_player_index = random.randint(0, NUMBER_OF_PLAYERS - 1)

    while True:
        current_player = players[current_player_index]
        print_board(board)
        
        move = input(f"Player {current_player}, choose a column (A-G): ").upper()

        if not is_valid_column(move):
            print("Invalid column. Please choose between A-G.")
            continue

        column_index = COLUMN_LABELS.index(move)

        if is_column_full(board, column_index):
            print("Column is full. Choose another one.")
            continue

        row, column = drop_piece(board, column_index, current_player)

        if is_winning_move(board, current_player, row, column):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUMBER_OF_PLAYERS

if __name__ == '__main__':
    play_game()
