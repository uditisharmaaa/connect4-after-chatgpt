import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + ' '.join(COL_LABELS))
    # Print rows
    for row in board:
        print('|'+ '|'.join(row) + '|')
    print('+' + '--'*COLS + '+')

def is_valid_column(col):
    return col in COL_LABELS

def get_col_index(col_char):
    return COL_LABELS.index(col_char)

def is_col_full(board, col_idx):
    return board[0][col_idx] != ' '

def drop_piece(board, col_idx, symbol):
    # Drop piece from bottom up
    for row_idx in reversed(range(ROWS)):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = symbol
            return row_idx, col_idx
    return None  # Should not happen if checked before

def check_win(board, symbol, row, col):
    # Check all directions from (row, col)
    def count_direction(r, c, dr, dc):
        count = 0
        r += dr
        c += dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        return count

    # 4 directions: horizontal, vertical, diagonal /
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        # count pieces in one direction + opposite + the current piece
        count = 1 + count_direction(row, col, dr, dc) + count_direction(row, col, -dr, -dc)
        if count >= 4:
            return True
    return False

def check_draw(board):
    # No more empty spaces in top row means board full
    return all(cell != ' ' for cell in board[0])

def get_num_players():
    while True:
        try:
            num = int(input("Enter number of players (2-5): "))
            if 2 <= num <= 5:
                return num
            else:
                print("Please enter a number between 2 and 5.")
        except:
            print("Invalid input, please enter a number.")

def get_player_move(player_symbol):
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").strip().upper()
        if not is_valid_column(move):
            print("Invalid column. Choose a letter A to G.")
            continue
        return move

def main():
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]

    board = create_board()
    current_player_idx = random.randint(0, num_players -1)

    while True:
        print_board(board)
        current_player_symbol = players[current_player_idx]

        while True:
            col_char = get_player_move(current_player_symbol)
            col_idx = get_col_index(col_char)
            if is_col_full(board, col_idx):
                print(f"Column {col_char} is full. Choose another column.")
            else:
                break

        row_placed, col_placed = drop_piece(board, col_idx, current_player_symbol)

        if check_win(board, current_player_symbol, row_placed, col_placed):
            print_board(board)
            print(f"Player {current_player_symbol} wins! Congratulations!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
