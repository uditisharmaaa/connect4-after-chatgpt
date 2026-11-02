import random
import os

# Constants for the board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS_COUNT = 2
PLAYER_LABELS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS_COUNT]

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_column_input():
    while True:
        column = input(f'Player {PLAYER_LABELS[current_player]}, please enter a column: ').strip().upper()
        if len(column) == 1 and 'A' <= column <= 'A' + str(COLUMNS - 1):
            col_index = ord(column) - 65
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full. Try another one.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, player_label):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_label
            break

def check_for_win(board, player_label):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_label for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_label for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_label for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_label for i in range(4)):
                return True
                
    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Initialize the game
board = create_board(ROWS, COLUMNS)
current_player = random.randint(0, PLAYERS_COUNT - 1)

print_board(board)

# Game loop
while True:
    col = get_column_input()
    place_checker(board, col, PLAYER_LABELS[current_player])
    print_board(board)

    if check_for_win(board, PLAYER_LABELS[current_player]):
        print(f'Player {PLAYER_LABELS[current_player]} won!')
        break
    elif check_for_draw(board):
        print('The game is a draw!')
        break

    # Switch player
    current_player = (current_player + 1) % PLAYERS_COUNT
