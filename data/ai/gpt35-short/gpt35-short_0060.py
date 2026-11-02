import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = 'A B C D E F G'.split()
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Allowed symbols for players
MIN_PLAYERS = 2
MAX_PLAYERS = 5

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMNS_LABELS))
    for row in board:
        print('| ' + ' '.join(row) + ' |')
    print('+' + '--'*COLS + '-+')

def is_valid_column(col_str):
    return col_str.upper() in COLUMNS_LABELS

def get_column_index(col_str):
    return COLUMNS_LABELS.index(col_str.upper())

def is_column_full(board, col):
    return board[0][col] != ' '

def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row, col  # return position where piece landed
    return None  # Should never happen if checked before!

def check_winner(board, piece, row, col):
    # Check all directions: horizontal, vertical, diagonal /
    
    def count_direction(delta_r, delta_c):
        count = 0
        r, c = row, col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r += delta_r
            c += delta_c
        return count - 1  # subtract current spot one time
    
    # Horizontal check
    horizontal_count = 1 + count_direction(0, 1) + count_direction(0, -1)
    if horizontal_count >= 4:
        return True
    
    # Vertical check
    vertical_count = 1 + count_direction(1, 0) + count_direction(-1, 0)
    if vertical_count >= 4:
        return True
    
    # Diagonal (main: \)
    diag1_count = 1 + count_direction(1, 1) + count_direction(-1, -1)
    if diag1_count >= 4:
        return True
    
    # Diagonal (anti: /)
    diag2_count = 1 + count_direction(1, -1) + count_direction(-1, 1)
    if diag2_count >= 4:
        return True
    
    return False

def board_full(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def get_num_players():
    while True:
        try:
            n = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= n <= MAX_PLAYERS:
                return n
        except ValueError:
            pass
        print(f"Invalid number of players. Please enter between {MIN_PLAYERS} and {MAX_PLAYERS}.")

def main():
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    current_idx = random.randrange(num_players)
    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {', '.join(players)}")
        current_player = players[current_idx]
        print(f"Player {current_player}'s turn.")
        
        col_str = input(f"Choose a column ({', '.join(COLUMNS_LABELS)}): ").strip().upper()
        if not is_valid_column(col_str):
            print(f"Invalid column. Please choose from {', '.join(COLUMNS_LABELS)}.")
            input("Press Enter to continue...")
            continue
        col = get_column_index(col_str)
        if is_column_full(board, col):
            print(f"Column {col_str} is full. Please choose another one.")
            input("Press Enter to continue...")
            continue
        
        row, col = drop_piece(board, col, current_player)
        if check_winner(board, current_player, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        if board_full(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw.")
            break

        current_idx = (current_idx + 1) % num_players

if __name__ == "__main__":
    main()
