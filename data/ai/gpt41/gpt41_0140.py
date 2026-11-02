import os
import random
import string

# Constants for the board and game settings
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set to 2 for submission

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(cols):
    return list(string.ascii_uppercase[:cols])

def get_player_input(current_player, valid_columns, board):
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if choice in valid_columns:
            col_index = valid_columns.index(choice)
            # Check if column is not full
            if board[0][col_index] == ' ':
                return col_index
            else:
                print("Column is full! You lose your turn.")
                return None  # Lose the turn if column is full
        else:
            print("Invalid column! Please enter a valid column letter.")

def drop_checker(board, col, player_symbol):
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row, col
    # Should never reach here if validated before
    return None

def check_line_win(line, symbol):
    count = 0
    for cell in line:
        if cell == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_win(board, player_symbol, last_row, last_col):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    if check_line_win([board[last_row][c] for c in range(cols)], player_symbol):
        return True

    # Vertical check
    if check_line_win([board[r][last_col] for r in range(rows)], player_symbol):
        return True

    # Diagonal (top-left to bottom-right)
    diag = []
    r, c = last_row, last_col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    while r < rows and c < cols:
        diag.append(board[r][c])
        r += 1
        c += 1
    if check_line_win(diag, player_symbol):
        return True

    # Anti-diagonal (bottom-left to top-right)
    anti_diag = []
    r, c = last_row, last_col
    while r < rows - 1 and c > 0:
        r += 1
        c -= 1
    while r >= 0 and c < cols:
        anti_diag.append(board[r][c])
        r -= 1
        c += 1
    if check_line_win(anti_diag, player_symbol):
        return True

    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])  # Top row all occupied

def main():
    board = create_board(ROWS, COLS)
    valid_columns = get_valid_columns(COLS)
    checkers = PLAYER_SYMBOLS[:NUM_PLAYERS]
    starting_player = random.randint(0, NUM_PLAYERS - 1)
    current_player_idx = starting_player

    clear_screen()
    print_board(board)

    moves = 0
    while True:
        player_symbol = checkers[current_player_idx]
        col_index = get_player_input(player_symbol, valid_columns, board)
        if col_index is None:
            # Lose turn if column was full
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        row, col = drop_checker(board, col_index, player_symbol)
        moves += 1

        clear_screen()
        print_board(board)
        if check_win(board, player_symbol, row, col):
            print(f"Player {player_symbol} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
