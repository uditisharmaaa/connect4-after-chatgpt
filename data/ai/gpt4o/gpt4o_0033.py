import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    """Creates an empty board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')
    print('  A   B   C   D   E   F   G ')
    for row in board:
        print('+---' * COLUMNS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLUMNS + '+')

def is_valid_input(input_str):
    """Checks if the input is a valid column letter."""
    return len(input_str) == 1 and 'A' <= input_str <= 'G'

def get_column_index(column_letter):
    """Converts a column letter (e.g., 'A') to a column index (e.g., 0)."""
    return ord(column_letter) - ord('A')

def make_move(board, player_symbol, column):
    """Attempts to place the player's checker in the specified column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False

def check_for_win(board, player_symbol):
    """Checks if the player has won the game."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
    return False

def check_for_draw(board):
    """Checks if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    """Main function to run the game."""
    board = create_board()
    current_turn = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_player = PLAYER_SYMBOLS[current_turn]
        column_input = ''
        while not is_valid_input(column_input):
            column_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        column_index = get_column_index(column_input)
        
        if not make_move(board, current_player, column_index):
            print("Column full! Turn lost.")
            continue

        print_board(board)

        if check_for_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_for_draw(board):
            print("It's a draw!")
            break

        current_turn = (current_turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
