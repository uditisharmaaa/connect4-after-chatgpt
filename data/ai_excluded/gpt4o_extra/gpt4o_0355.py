import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # adjust number of players here
WIN_CONDITION = 4

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join([chr(65 + i) for i in range(len(board[0]))])
    print(header)
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * len(board[0]) + '+')

def get_column_index(column_letter):
    return ord(column_letter.upper()) - ord('A')

def is_valid_input(input_str, columns):
    return len(input_str) == 1 and input_str.isalpha() and 'A' <= input_str <= chr(65 + columns - 1)

def place_checker(board, column_index, symbol):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = symbol
            return True
    return False

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for row in board:
        for col in range(cols - WIN_CONDITION + 1):
            if all(cell == symbol for cell in row[col:col + WIN_CONDITION]):
                return True

    # Vertical check
    for col in range(cols):
        for row in range(rows - WIN_CONDITION + 1):
            if all(board[row + i][col] == symbol for i in range(WIN_CONDITION)):
                return True

    # Positive diagonal check
    for row in range(rows - WIN_CONDITION + 1):
        for col in range(cols - WIN_CONDITION + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_CONDITION)):
                return True

    # Negative diagonal check
    for row in range(WIN_CONDITION - 1, rows):
        for col in range(cols - WIN_CONDITION + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board(ROWS, COLUMNS)
    players = random.sample(PLAYER_SYMBOLS[:NUM_PLAYERS], NUM_PLAYERS)
    current_player_index = 0

    print_board(board)

    while True:
        current_player_symbol = players[current_player_index]
        print(f"Player {current_player_symbol}, please enter a column:")

        while True:
            user_input = input().strip()
            if is_valid_input(user_input, COLUMNS):
                column_index = get_column_index(user_input)
                if place_checker(board, column_index, current_player_symbol):
                    break
                else:
                    print("Column is full. Choose again:")
            else:
                print("Invalid input. Choose again:")

        print_board(board)

        if check_win(board, current_player_symbol):
            print(f"Player {current_player_symbol} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
