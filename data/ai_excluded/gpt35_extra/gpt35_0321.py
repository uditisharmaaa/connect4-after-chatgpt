import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players allowed

def clear_screen():
    os.system('clear')

def create_board():
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print('  ' + '   '.join(letters))
    # Print board with lines
    for row in range(ROWS):
        print('+' + '---+' * COLUMNS)
        row_str = '|'
        for col in range(COLUMNS):
            row_str += ' ' + board[row][col] + ' |'
        print(row_str)
    print('+' + '---+' * COLUMNS)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + COLUMNS -1):
        return True
    return False

def column_index(col_char):
    return ord(col_char.upper()) - ord('A')

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Start from bottom row upwards, place in first empty cell
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    # Should not happen if checked is_column_full before
    return -1

def check_winner(board, row, col, checker):
    # Directions: horizontal, vertical, diagonal /
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down right
        (1, -1)   # diagonal down left
    ]
    for dr, dc in directions:
        count = 1  # count checker itself
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        current_checker = players[current_player_index]
        # Input loop
        while True:
            print(f'Player {current_checker}, please enter a column:')
            inp = input().strip().upper()
            if not is_valid_column(inp):
                print('Invalid input. Please enter a valid column letter.')
                continue
            col = column_index(inp)
            if is_column_full(board, col):
                print('Column is full. You lose your turn.')
                break  # lose turn if column full
            else:
                row = place_checker(board, col, current_checker)
                break
        print_board(board)
        # If placed checker, check win
        if not is_column_full(board, col):
            if check_winner(board, row, col, current_checker):
                print(f'Player {current_checker} won!')
                break
        # Check draw
        if board_full(board):
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == '__main__':
    main()
