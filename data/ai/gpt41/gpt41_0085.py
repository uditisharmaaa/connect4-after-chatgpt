import os
import random
import string

# --- Constants ---
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set to required number (2 in your submission)
CONNECT_N = 4

# --- Functions ---
def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    col_labels = list(string.ascii_uppercase[:COLS])
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def get_valid_column_input(prompt, board):
    valid_cols = set(string.ascii_uppercase[:COLS])
    while True:
        col = input(prompt).strip().upper()
        if len(col) != 1 or col not in valid_cols:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col_idx = ord(col) - ord('A')
        if board[0][col_idx] != ' ':
            print("That column is full. You lose your turn.")
            return None
        return col_idx

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return board.index(row), col  # return position for win-check
    return None, None  # Should not occur if checked before

def check_win(board, row, col, checker):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row, col
            while True:
                r += dr*step
                c += dc*step
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                    if count >= CONNECT_N:
                        return True
                else:
                    break
    return False

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    player_ids = list(range(NUM_PLAYERS))
    player_symbols = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(player_ids)
    clear_screen()
    print_board(board)

    while True:
        checker = player_symbols[current_player]
        print(f"Player {checker}, please enter a column:")
        col = get_valid_column_input("> ", board)
        if col is None:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        row, col_ = place_checker(board, col, checker)
        clear_screen()
        print_board(board)
        if check_win(board, row, col_, checker):
            print(f"Player {checker} won!")
            break
        if is_board_full(board):
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
