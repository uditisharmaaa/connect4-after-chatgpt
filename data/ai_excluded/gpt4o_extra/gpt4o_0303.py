import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')
    print()

def is_valid_column(column_input):
    if len(column_input) != 1:
        return False
    if column_input < 'A' or column_input > chr(ord('A') + COLUMNS - 1):
        return False
    return True

def column_to_index(column_input):
    return ord(column_input) - ord('A')

def place_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return True
    return False

def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    num_players = 2
    player_symbols = PLAYER_SYMBOLS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)
    
    while True:
        print_board(board)
        current_symbol = player_symbols[current_player_idx]
        column_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()

        if not is_valid_column(column_input):
            print("Invalid input. Try again.")
            input("Press Enter to continue...")
            continue

        column = column_to_index(column_input)

        if not place_checker(board, column, current_symbol):
            print("Column full or invalid. Turn forfeited.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        if check_win(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
