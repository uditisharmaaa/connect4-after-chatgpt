import os
import random
import string

# ==== Constants ====
ROWS = 6
COLS = 7
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2   # Change this number up to 5 for more players

# ========== Functions ==========

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    col_labels = '   ' + '   '.join([string.ascii_uppercase[c] for c in range(COLS)])
    print(col_labels)
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def valid_column(col_input):
    return len(col_input) == 1 and col_input.isalpha() and col_input.upper() < chr(ord('A')+COLS)

def get_column_index(col_input):
    return ord(col_input.upper()) - ord('A')

def find_row_for_col(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            return row
    return None

def is_board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def check_winner(board, row, col, player_char):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1)   # diag down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_char:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_char:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# ========== Main Game Loop ==========

def main():
    board = create_board()
    players = PLAYER_CHARS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        player = players[current]
        # Prompt
        col_input = input(f"Player {player}, please enter a column: ").strip().upper()
        # Input validation loop
        while not valid_column(col_input) or find_row_for_col(board, get_column_index(col_input)) is None:
            if not valid_column(col_input):
                col_input = input("Invalid column. Please enter a valid column (A-G): ").strip().upper()
            else:
                # Check if column is full
                print("Column is full. You lose your turn.")
                current = (current + 1) % NUM_PLAYERS
                break
        else:
            col = get_column_index(col_input)
            row = find_row_for_col(board, col)
            board[row][col] = player
            print_board(board)
            if check_winner(board, row, col, player):
                print(f"Player {player} won!")
                break
            elif is_board_full(board):
                print("Game is a draw!")
                break
            current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
