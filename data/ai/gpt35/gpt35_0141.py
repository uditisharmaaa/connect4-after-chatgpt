import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(ord('A')+i) for i in range(COLS)))
    print('+---'*COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+---'*COLS + '+')

def valid_column(col):
    return col.isalpha() and col >= 'A' and col < chr(ord('A')+COLS)

def place_checker(board, col, checker):
    c = ord(col) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == ' ':
            board[r][c] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)

    while True:
        checker = players[current]
        col = input(f'Player {checker}, please enter a column: ').strip().upper()
        if not valid_column(col):
            continue
        if not place_checker(board, col, checker):
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, checker):
            print(f'Player {checker} won!')
            break
        if check_draw(board):
            print('The game is a draw.')
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
