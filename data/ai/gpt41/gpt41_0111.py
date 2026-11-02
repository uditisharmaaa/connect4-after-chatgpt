import os
import random
import string

# --------------- CONSTANTS -----------------
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # Use values from 2 to 5

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
BOARD_EMPTY_CHAR = ' '

WIN_SEQUENCE = 4

COLUMN_LABELS = list(string.ascii_uppercase)

# --------------- FUNCTIONS -----------------

def clear_screen():
    os.system('clear')  # For Unix/Linux/Mac
    # os.system('cls')  # Uncomment for Windows

def create_board(rows, cols):
    return [[BOARD_EMPTY_CHAR for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    label_row = '  ' + '   '.join(COLUMN_LABELS[:cols])
    sep = '+' + '---+' * cols
    print(label_row)
    for row in board:
        print(sep)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(sep)

def get_valid_columns(board):
    valid = []
    cols = len(board[0])
    rows = len(board)
    for col in range(cols):
        if board[0][col] == BOARD_EMPTY_CHAR:
            valid.append(COLUMN_LABELS[col])
    return valid

def get_move(board, player_symbol):
    cols = len(board[0])
    valid_cols = get_valid_columns(board)
    prompt = f"Player {player_symbol}, please enter a column ({'/'.join(valid_cols)}): "
    while True:
        move = input(prompt).strip().upper()
        if len(move) != 1 or move not in COLUMN_LABELS[:cols]:
            print("Invalid input! Please enter a valid column label (A-G).")
            continue
        if move not in valid_cols:
            print(f"Column {move} is full! You lose your turn.")
            return None  # Indicate turn lost
        return COLUMN_LABELS.index(move)

def place_checker(board, column, symbol):
    rows = len(board)
    for i in range(rows-1, -1, -1):
        if board[i][column] == BOARD_EMPTY_CHAR:
            board[i][column] = symbol
            return i, column  # return position
    return None  # Should not occur if logic above is used.

def check_win(board, row, col, symbol):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1),  # Diagonal /
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction (dr, dc)
        r, c = row + dr, col + dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in negative direction (-dr, -dc)
        r, c = row - dr, col - dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_SEQUENCE:
            return True
    return False

def in_bounds(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def is_draw(board):
    return all(board[0][col] != BOARD_EMPTY_CHAR for col in range(len(board[0])))

def switch_player(cur, total_players):
    return (cur + 1) % total_players

# --------------- MAIN GAME -----------------

def main():
    assert 2 <= NUM_PLAYERS <= 5, "Player number must be between 2 and 5"
    assert COLUMNS <= 26, "Cannot support more than 26 columns"

    board = create_board(ROWS, COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)
    print(f"Player {players[current_player]} will start!\n")

    while True:
        print()
        symbol = players[current_player]
        valid_cols = get_valid_columns(board)

        if not valid_cols:
            # All columns are full
            print("Game is a draw!")
            break

        move = get_move(board, symbol)
        clear_screen()

        if move is None:
            print_board(board)
            print(f"Player {symbol} lost the turn (no checker placed).")
            current_player = switch_player(current_player, NUM_PLAYERS)
            continue

        row, col = place_checker(board, move, symbol)
        print_board(board)

        if check_win(board, row, col, symbol):
            print(f"Player {symbol} won!")
            break
        elif is_draw(board):
            print("Game is a draw!")
            break
        current_player = switch_player(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
