import os, random, sys

# Constants (submission requires 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
LETTERS = [chr(ord('A') + i) for i in range(COLS)]

def create_board(r, c):
    return [[' ' for _ in range(c)] for _ in range(r)]

def render(board):
    os.system('clear')
    header = '  ' + '   '.join(LETTERS)
    print(header)
    horiz = '+' + '---+' * COLS
    for r in range(ROWS):
        print(horiz)
        row = '|' + '|'.join(f' {board[r][c]} ' for c in range(COLS)) + '|'
        print(row)
    print(horiz)

def valid_letter(s):
    return len(s) == 1 and 'A' <= s <= chr(ord('A') + COLS - 1)

def get_column_input(player_token):
    while True:
        try:
            s = input(f'Player {player_token}, please enter a column: ').strip().upper()
        except EOFError:
            sys.exit(0)
        if not valid_letter(s):
            continue
        return ord(s) - ord('A'), s

def drop_checker(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r
    return None

def check_win(board, token):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + k] == token for k in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + k][c] == token for k in range(4)):
                return True
    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + k][c + k] == token for k in range(4)):
                return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - k][c + k] == token for k in range(4)):
                return True
    return False

def board_full(board):
    return all(board[r][c] != ' ' for r in range(ROWS) for c in range(COLS))

def main():
    if not (2 <= NUM_PLAYERS <= 5) or not (1 <= COLS <= 26):
        print("Invalid configuration.")
        return
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    render(board)
    while True:
        token = TOKENS[current]
        col_idx, col_letter = get_column_input(token)
        row = drop_checker(board, col_idx, token)
        if row is None:
            # Column full: turn is lost
            print(f'Column {col_letter} is full. Turn lost.')
            current = (current + 1) % NUM_PLAYERS
            continue
        render(board)
        if check_win(board, token):
            print(f'Player {token} won!')
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
