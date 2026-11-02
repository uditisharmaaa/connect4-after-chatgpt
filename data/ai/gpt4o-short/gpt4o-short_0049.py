import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change this to 2, 3, 4, or 5

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '  '.join(COLUMN_LABELS))
    for row in board:
        print(' | '.join(row))
        print('-' * (COLUMNS * 3 - 1))

def get_player_input(current_player):
    while True:
        column = input(f"Player {current_player}, choose a column (A-G): ").upper()
        if column in COLUMN_LABELS:
            return COLUMN_LABELS.index(column)
        else:
            print("Invalid input. Please choose a column between A and G.")

def make_move(board, column, player):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            return True
    return False

def check_for_win(board, player):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check diagonal (bottom left to top right) win
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonal (top left to bottom right) win
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_index]

    while True:
        print_board(board)
        column = get_player_input(current_player)

        if not make_move(board, column, current_player):
            print("Column is full, try another one.")
            continue

        if check_for_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_for_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
