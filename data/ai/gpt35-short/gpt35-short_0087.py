import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
MIN_PLAYERS = 2
MAX_PLAYERS = 5

def clear_screen():
    os.system('clear')

def create_board():
    # Create empty board represented by spaces
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + ' '.join(COLUMN_LABELS))
    # Print each row
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+-----------------+')

def get_num_players():
    while True:
        try:
            n = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= n <= MAX_PLAYERS:
                return n
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Enter a number.")

def get_player_move(player_symbol):
    while True:
        move = input(f"Player '{player_symbol}' turn - Choose column (A-G): ").strip().upper()
        if move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid column. Please choose a letter from A to G.")

def is_valid_move(board, col):
    # Check if top of column is empty (meaning column not full)
    return board[0][col] == ' '

def make_move(board, col, symbol):
    # Drop symbol to the lowest empty spot in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col

def check_win(board, symbol):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == symbol for i in range(4)):
                return True
    # Check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == symbol for i in range(4)):
                return True
    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == symbol for i in range(4)):
                return True
    # Check diagonal down-left
    for r in range(ROWS - 3):
        for c in range(3, COLUMNS):
            if all(board[r+i][c-i] == symbol for i in range(4)):
                return True
    return False

def check_draw(board):
    # Draw if no empty spots in top row
    return all(space != ' ' for space in board[0])

def main():
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]

    # Randomize first player
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        print_board(board)

        current_symbol = players[current_player_idx]

        # Get valid column
        while True:
            col = get_player_move(current_symbol)
            if is_valid_move(board, col):
                break
            else:
                print("Column full! Choose a different column.")

        # Make the move
        row, col = make_move(board, col, current_symbol)

        print_board(board)

        # Check win
        if check_win(board, current_symbol):
            print(f"Player '{current_symbol}' wins! Congratulations!")
            break

        # Check draw
        if check_draw(board):
            print("Game ended in a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
