import os
import random
import string

# ===== Configuration =====
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set between 2 and 5 inclusive
WIN_CONDITION = 4
PLAYER_CHEKERS = ['X', 'O', 'V', 'H', 'M']

# ===== Initialization =====
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = '  '.join(string.ascii_uppercase[:len(board[0])])
    print('  ' + col_labels)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

# ===== Input Validation =====
def get_player_input(board, player):
    cols = len(board[0])
    valid_labels = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        inp = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = valid_labels.index(inp)
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full! You lose your turn.")
            return None
        return col

# ===== Placing Checkers =====
def place_checker(board, col, checker):
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # Return row, col where checker was placed

# ===== Win Checking =====
def check_win(board, row, col, checker):
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # right, down, down-right, down-left
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

# ===== Game Loop =====
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    checkers = PLAYER_CHEKERS[:NUM_PLAYERS]
    players = list(range(NUM_PLAYERS))
    current = random.choice(players)
    print_board(board)
    while True:
        checker = checkers[current]
        col = get_player_input(board, checker)
        if col is None:
            current = (current + 1) % NUM_PLAYERS
            continue
        row, col = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
