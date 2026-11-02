import os
import random

# Constants for player tokens
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Create the game board
ROWS = 6
COLUMNS = 7
EMPTY_SLOT = '.'
COLUMN_LABELS = "ABCDEFG"

def create_board():
    return [[EMPTY_SLOT for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print(' ' + ' '.join(row))

def is_valid_input(column, board):
    return column in COLUMN_LABELS and board[0][COLUMN_LABELS.index(column)] == EMPTY_SLOT

def find_first_empty_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY_SLOT:
            return row
    return -1  # Should not happen if input is valid

def place_token(board, column, token):
    col_index = COLUMN_LABELS.index(column)
    row_index = find_first_empty_row(board, col_index)
    board[row_index][col_index] = token

def is_winning_move(board, token):
    # Check horizontal, vertical and diagonal lines for a win.
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == token for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[0][col] != EMPTY_SLOT for col in range(COLUMNS))

def main():
    num_players = int(input("Enter the number of players (2-5): "))
    players = PLAYER_TOKENS[:num_players]

    board = create_board()
    current_player_index = random.randint(0, num_players - 1)

    while True:
        print_board(board)
        current_player = players[current_player_index]
        column = input(f"Player {current_player}, choose a column (A-G): ").upper()

        while not is_valid_input(column, board):
            column = input("Invalid input. Choose a valid column (A-G): ").upper()

        place_token(board, column, current_player)

        if is_winning_move(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
