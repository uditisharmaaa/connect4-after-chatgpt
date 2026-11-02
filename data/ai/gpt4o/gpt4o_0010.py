import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
MAX_COLUMNS = 26
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers
    column_labels = ' '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    
    # Print board with row dividers
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def is_valid_input(input_value, columns):
    # Check if input is a valid column label
    if len(input_value) != 1 or not input_value.isalpha():
        return False
    input_index = ord(input_value.upper()) - ord('A')
    return 0 <= input_index < columns

def get_lowest_empty_row(board, column):
    # Finds the lowest empty row index for a given column
    for row in reversed(range(len(board))):
        if board[row][column] == ' ':
            return row
    return None

def check_win(board, symbol):
    # Check horizontal, vertical, and diagonal wins
    rows = len(board)
    columns = len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    
    # Check diagonals (top-left to bottom-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    # Check if all columns are filled
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def main():
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    print_board(board)

    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        current_player_symbol = PLAYER_SYMBOLS[current_player_idx]
        print(f"Player {current_player_symbol}, please enter a column:")
        
        user_input = input().strip().upper()

        # Validate user input
        if is_valid_input(user_input, BOARD_COLUMNS):
            column_index = ord(user_input) - ord('A')
            lowest_row = get_lowest_empty_row(board, column_index)

            if lowest_row is not None:
                # Place the checker
                board[lowest_row][column_index] = current_player_symbol
                print_board(board)

                # Check for a win
                if check_win(board, current_player_symbol):
                    print(f"Player {current_player_symbol} won!")
                    break

                # Check for a draw
                if check_draw(board):
                    print("The game is a draw!")
                    break

                # Alternate player's turn
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            else:
                print("Column full. Player loses turn.")
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
