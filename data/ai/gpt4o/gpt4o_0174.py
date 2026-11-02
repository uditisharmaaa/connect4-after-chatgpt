import random
import os

ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
TO_WIN = 4
EMPTY_CELL = " "
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def initialize_board(rows, columns):
    return [[EMPTY_CELL for _ in range(columns)] for _ in range(rows)]

def is_valid_column(input_str, columns):
    return input_str.isalpha() and len(input_str) == 1 and ord(input_str.upper()) - 65 < columns

def get_lowest_empty_row(column, board):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == EMPTY_CELL:
            return r
    return None

def check_for_win(board, player_symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - TO_WIN + 1):
            if all(board[row][col + i] == player_symbol for i in range(TO_WIN)):
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - TO_WIN + 1):
            if all(board[row + i][col] == player_symbol for i in range(TO_WIN)):
                return True

    # Diagonal (bottom-left to top-right) check
    for row in range(ROWS - TO_WIN + 1):
        for col in range(COLUMNS - TO_WIN + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(TO_WIN)):
                return True

    # Diagonal (top-left to bottom-right) check
    for row in range(TO_WIN - 1, ROWS):
        for col in range(COLUMNS - TO_WIN + 1):
            if all(board[row - i][col + i] == player_symbol for i in range(TO_WIN)):
                return True

    return False

def check_for_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLUMNS))

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    num_players = 2
    players = PLAYER_SYMBOLS[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_player_symbol = players[current_player_index]
        column_input = input(f"Player {current_player_symbol}, please enter a column: ").strip().upper()
        
        if not is_valid_column(column_input, COLUMNS):
            print("Invalid input. Please enter a letter from A to G.")
            continue

        column_index = ord(column_input) - 65
        row_index = get_lowest_empty_row(column_index, board)

        if row_index is None:
            print("Column full! You lose your turn.")
            current_player_index = (current_player_index + 1) % num_players
            continue

        board[row_index][column_index] = current_player_symbol
        print_board(board)

        if check_for_win(board, current_player_symbol):
            print(f"Player {current_player_symbol} won!")
            break

        if check_for_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    play_game()
