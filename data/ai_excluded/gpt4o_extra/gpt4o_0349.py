import os
import random

# Constants
NUM_COLUMNS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def initialize_board(columns, rows):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    clear_screen()
    column_labels = ' '.join([chr(65 + i) for i in range(columns)])
    print(f"  {column_labels}")
    for row in board:
        print(f"+{'---+' * columns}")
        print(f"| {' | '.join(row)} |")
    print(f"+{'---+' * columns}")

def get_user_input(columns):
    while True:
        user_input = input("Please enter a column: ").upper()
        if user_input in [chr(65 + i) for i in range(columns)]:
            return ord(user_input) - 65
        print("Invalid input. Try again.")

def get_lowest_empty_row(board, col):
    for row in reversed(board):
        if row[col] == ' ':
            return board.index(row)
    return None

def place_checker(board, col, symbol):
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = symbol
        return True
    return False

def check_winner(board, symbol):
    # Horizontal Check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if board[row][col:col+4] == [symbol] * 4:
                return True

    # Vertical Check
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Diagonal Check
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True
        for col in range(3, NUM_COLUMNS):
            if all(board[row+i][col-i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(NUM_COLUMNS, NUM_ROWS)
    current_player_index = random.choice(range(NUM_PLAYERS))
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    while True:
        print_board(board, NUM_COLUMNS)
        print(f"Player {player_symbols[current_player_index]}, it is your turn.")
        column_choice = get_user_input(NUM_COLUMNS)

        if place_checker(board, column_choice, player_symbols[current_player_index]):
            if check_winner(board, player_symbols[current_player_index]):
                print_board(board, NUM_COLUMNS)
                print(f"Player {player_symbols[current_player_index]} won!")
                break
            if is_draw(board):
                print_board(board, NUM_COLUMNS)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
