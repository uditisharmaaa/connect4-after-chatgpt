import os
import random

ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear():
    os.system('clear')

def print_board(board):
    print(' ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def is_valid_column(col):
    return 0 <= col < COLS

def get_next_open_row(board, col):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # vertical
    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # positively sloped diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    # negatively sloped diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    # Draw if no empty spots in top row
    return all(board[0][c] != ' ' for c in range(COLS))

def get_player_count():
    while True:
        count_str = input('Enter number of players (2-5): ')
        if count_str.isdigit():
            count = int(count_str)
            if 2 <= count <=5:
                return count
        print('Invalid number. Please enter a number between 2 and 5.')

def get_column_input(player_piece):
    while True:
        col_str = input(f"Player {player_piece}, choose column (A-G): ").upper()
        if col_str in COLUMN_LABELS:
            col = COLUMN_LABELS.index(col_str)
            return col
        else:
            print("Invalid column. Choose a letter from A to G.")

def main():
    player_count = get_player_count()
    players = PLAYERS[:player_count]
    board = create_board()
    current_player_idx = random.randint(0, player_count - 1)

    while True:
        clear()
        print_board(board)
        current_piece = players[current_player_idx]

        col = get_column_input(current_piece)

        row = get_next_open_row(board, col)
        if row is None:
            print("Column full. Try a different column.")
            input("Press Enter to continue...")
            continue

        drop_piece(board, row, col, current_piece)

        if winning_move(board, current_piece):
            clear()
            print_board(board)
            print(f"Player {current_piece} wins!")
            break

        if is_draw(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % player_count

if __name__ == '__main__':
    main()
