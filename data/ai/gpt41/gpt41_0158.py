import random
import os
import string

# Constants for board dimensions and players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # You can change this for testing to 3, 4, or 5

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    cols = len(board[0])
    # Print column letters
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_valid_columns(board):
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def get_player_input(player, valid_cols, board):
    cols = len(board[0])
    col_letters = string.ascii_uppercase[:cols]
    while True:
        choice = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(choice) != 1 or choice not in col_letters:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = col_letters.index(choice)
        if board[0][col] != " ":
            print("This column is full! You lose your turn.")
            return None
        return col

def place_checker(board, col, symbol):
    # Place from bottom row up
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row, col
    return None  # Shouldn't reach here if col not full

def is_board_full(board):
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    four = 4  # how many in a row to win

    # Horizontal check
    for r in range(rows):
        for c in range(cols - (four - 1)):
            if all(board[r][c + i] == symbol for i in range(four)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - (four - 1)):
            if all(board[r + i][c] == symbol for i in range(four)):
                return True

    # Diagonal (down-right)
    for r in range(rows - (four - 1)):
        for c in range(cols - (four - 1)):
            if all(board[r + i][c + i] == symbol for i in range(four)):
                return True

    # Diagonal (up-right)
    for r in range(four - 1, rows):
        for c in range(cols - (four - 1)):
            if all(board[r - i][c + i] == symbol for i in range(four)):
                return True

    return False

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    # Choose who goes first
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        player_symbol = players[current_player]
        valid_cols = get_valid_columns(board)
        col = get_player_input(player_symbol, valid_cols, board)
        clear_screen()
        if col is None:
            # Column full, lose turn
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        row, _ = place_checker(board, col, player_symbol)
        print_board(board)
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
