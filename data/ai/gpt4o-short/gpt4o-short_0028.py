import os
import random

# Constants
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Change this number between 2 and 5 to set different player counts
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = 'ABCDEFG'

# Functions

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the console screen
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')

def get_player_input(player):
    while True:
        column_label = input(f"Player {player} ({PLAYER_TOKENS[player]}), enter column (A-G): ").upper()
        if column_label in COLUMN_LABELS:
            return COLUMN_LABELS.index(column_label)
        print("Invalid input. Please enter a valid column letter.")

def place_token(board, token, column):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = token
            return True
    return False

def check_winner(board, token):
    # Check horizontal, vertical, and diagonal conditions for a win
    for row in range(ROWS):
        for col in range(COLUMNS):
            # Check horizontal
            if col + 3 < COLUMNS and all(board[row][col+i] == token for i in range(4)):
                return True
            # Check vertical
            if row + 3 < ROWS and all(board[row+i][col] == token for i in range(4)):
                return True
            # Check diagonal (positive slope)
            if row + 3 < ROWS and col + 3 < COLUMNS and all(board[row+i][col+i] == token for i in range(4)):
                return True
            # Check diagonal (negative slope)
            if row - 3 >= 0 and col + 3 < COLUMNS and all(board[row-i][col+i] == token for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    players = random.sample(range(NUM_PLAYERS), NUM_PLAYERS)
    board = create_board()
    current_player_idx = 0

    while True:
        print_board(board)
        current_player = players[current_player_idx]
        column = get_player_input(current_player)

        if not place_token(board, PLAYER_TOKENS[current_player], column):
            print("Column is full. Choose another column.")
            continue

        if check_winner(board, PLAYER_TOKENS[current_player]):
            print_board(board)
            print(f"Player {current_player} ({PLAYER_TOKENS[current_player]}) wins!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# Main flow
if __name__ == "__main__":
    play_game()
