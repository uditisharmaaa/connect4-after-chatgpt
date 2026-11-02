import os
import random

# Constants for game settings
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 3  # Number of players, can be adjusted between 2 and 5
BLANK = '.'

def initialize_board():
    return [[BLANK for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def display_board(board):
    os.system('clear')
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print()

def get_valid_column_input():
    valid_input = False
    while not valid_input:
        column = input(f"Choose a column ({', '.join(COLUMN_LABELS)}): ").strip().upper()
        if column in COLUMN_LABELS:
            return COLUMN_LABELS.index(column)
        print("Invalid input. Please enter a valid column letter.")

def is_column_full(board, column_index):
    return all(row[column_index] != BLANK for row in board)

def drop_piece(board, column_index, player):
    for row in reversed(board):
        if row[column_index] == BLANK:
            row[column_index] = player
            return

def check_victory(board, player):
    # Check horizontal, vertical, and diagonal (both directions)
    def check_four_in_a_row(sequence):
        return any(sequence[i:i+4] == [player] * 4 for i in range(len(sequence) - 3))

    # Check horizontal
    for row in board:
        if check_four_in_a_row(row):
            return True

    # Check vertical
    for col in range(NUM_COLUMNS):
        column = [board[row][col] for row in range(NUM_ROWS)]
        if check_four_in_a_row(column):
            return True

    # Check diagonal (positive slope)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            diagonal = [board[row + i][col + i] for i in range(4)]
            if diagonal == [player] * 4:
                return True

    # Check diagonal (negative slope)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            diagonal = [board[row - i][col + i] for i in range(4)]
            if diagonal == [player] * 4:
                return True

    return False

def check_draw(board):
    return all(board[0][col] != BLANK for col in range(NUM_COLUMNS))

def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        display_board(board)
        print(f"Player {PLAYERS[current_player_index]}'s turn.")

        column_index = get_valid_column_input()
        if is_column_full(board, column_index):
            print("Column full. Choose another column.")
            continue

        drop_piece(board, column_index, PLAYERS[current_player_index])

        if check_victory(board, PLAYERS[current_player_index]):
            display_board(board)
            print(f"Player {PLAYERS[current_player_index]} wins!")
            break

        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        # Cycle to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
