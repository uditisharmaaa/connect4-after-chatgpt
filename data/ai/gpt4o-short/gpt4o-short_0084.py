import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # You can change this to 2, 3, 4, or 5

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    print(' +-------------+')
    for row in board:
        print(' |' + '|'.join(row) + '|')
    print(' +-------------+')

def check_input(column_input, current_player):
    if column_input not in 'ABCDEFG':
        print(f"Invalid input. Player {PLAYER_SYMBOLS[current_player]}, please enter a valid column (A-G).")
        return False
    return True

def drop_piece(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = PLAYER_SYMBOLS[player]
            return True
    return False

def check_winner(board):
    # Check horizontal, vertical, and diagonal wins

    # Horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != ' ':
                return True

    # Vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != ' ':
                return True

    # Diagonal win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != ' ':
                return True
            if board[row][col + 3] == board[row + 1][col + 2] == board[row + 2][col + 1] == board[row + 3][col] != ' ':
                return True

    return False

def check_draw(board):
    return all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLUMNS))

def play_game():
    board = create_board(ROWS, COLUMNS)
    players = [i for i in range(NUM_PLAYERS)]
    random.shuffle(players)

    print_board(board)
    current_player = 0

    while True:
        print(f"Player {PLAYER_SYMBOLS[players[current_player] % NUM_PLAYERS]}'s turn.")
        column_input = input('Choose a column (A-G): ').upper()

        if not check_input(column_input, players[current_player] % NUM_PLAYERS):
            continue

        column = ord(column_input) - ord('A')

        if not drop_piece(board, column, players[current_player] % NUM_PLAYERS):
            print(f"Column {column_input} is full. Try another one.")
            continue

        print_board(board)

        if check_winner(board):
            print(f"Player {PLAYER_SYMBOLS[players[current_player] % NUM_PLAYERS]} wins!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    play_game()
