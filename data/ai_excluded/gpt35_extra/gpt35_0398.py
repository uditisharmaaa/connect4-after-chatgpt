import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2

# For submission: 2 players, 6x7 board
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(labels))
    # Print board rows with borders
    line = '+---' * len(board[0]) + '+'
    for row in board:
        print(line)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(line)

def input_column(player, board):
    cols = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(cols)]
    while True:
        entry = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(entry) != 1:
            # Invalid input length
            continue
        if entry not in valid_cols:
            # Invalid column letter
            continue
        col_index = ord(entry) - ord('A')
        # Check if column is full
        if board[0][col_index] != ' ':
            # Column full -> lose turn
            return None
        return col_index

def place_checker(board, col, checker):
    # Place checker at lowest empty row in column col
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # Check vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # Check diagonal / (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(3, cols):
            if (board[r][c] == checker and
                board[r+1][c-1] == checker and
                board[r+2][c-2] == checker and
                board[r+3][c-3] == checker):
                return True
    # Check diagonal \ (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
    return False

def check_draw(board):
    # If top row has any empty, not draw
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    turn = random.randint(0, NUM_PLAYERS -1)

    print_board(board)

    while True:
        player_checker = players[turn]
        col = input_column(player_checker, board)
        if col is None:
            # Column full: lose turn, just print board and next turn
            print_board(board)
            turn = (turn + 1) % NUM_PLAYERS
            continue
        place_checker(board, col, player_checker)
        print_board(board)
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
