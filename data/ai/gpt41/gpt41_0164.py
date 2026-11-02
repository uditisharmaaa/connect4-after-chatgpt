import os
import random
import string

# --- Constants ---
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_COLS = 26
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
N_PLAYERS = 2                     # Change this value (2-5) for different number of players
WIN_LENGTH = 4

# --- Functions ---

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(letters))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {0} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def get_player_symbols(n):
    return PLAYER_SYMBOLS[:n]

def get_valid_columns(board):
    return [i for i in range(len(board[0])) if board[0][i] == ' ']

def get_column_from_input(input_str, board):
    input_str = input_str.strip().upper()
    if len(input_str) != 1:
        return None
    letter = input_str[0]
    if letter < 'A' or letter >= chr(ord('A') + len(board[0])):
        return None
    return ord(letter) - ord('A')

def get_lowest_empty_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])

def check_win(board, symbol):
    rows, cols = len(board), len(board[0])
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    # Check diagonal (\)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    # Check anti-diagonal (/)
    for row in range(WIN_LENGTH-1, rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    return False

def play_game():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    player_symbols = get_player_symbols(N_PLAYERS)
    current_player = random.randint(0, N_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        player_symbol = player_symbols[current_player]
        print(f"Player {player_symbol}, please enter a column:")

        col = None
        while True:
            user_input = input("> ")
            col = get_column_from_input(user_input, board)
            if col is None:
                print("Invalid input. Please enter a valid column letter.")
                continue
            if board[0][col] != ' ':
                print("Column is full. You lose your turn.")
                col = None
                break
            break

        # If column is full, skip to next player (turn lost)
        if col is None:
            current_player = (current_player + 1) % N_PLAYERS
            clear_screen()
            print_board(board)
            continue

        row = get_lowest_empty_row(board, col)
        board[row][col] = player_symbol

        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % N_PLAYERS

# --- Main Execution ---
if __name__ == "__main__":
    play_game()
