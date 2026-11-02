import os
import random

# Constants
NUM_PLAYERS = 2
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(COLUMN_LABELS[:COLUMNS]))
    for row in range(ROWS):
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(board[row]) + ' |')
    print('+---' * COLUMNS + '+')

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def get_random_player():
    return random.choice(range(NUM_PLAYERS))

def place_checker(board, col, marker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = marker
            return True
    return False

def check_win(board, marker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == marker for i in range(4)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == marker for i in range(4)):
                return True

    # Diagonal check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == marker for i in range(4)):
                return True
    
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == marker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = initialize_board()
    current_player = get_random_player()
    print_board(board)

    while True:
        print("Player {}, please enter a column:".format(PLAYER_MARKERS[current_player]))
        col_input = input().strip().upper()

        if col_input not in COLUMN_LABELS[:COLUMNS]:
            print("Invalid input, try again!")
            continue

        col = COLUMN_LABELS.index(col_input)

        if not place_checker(board, col, PLAYER_MARKERS[current_player]):
            print("Column is full! You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        print_board(board)

        if check_win(board, PLAYER_MARKERS[current_player]):
            print("Player {} won!".format(PLAYER_MARKERS[current_player]))
            break

        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
