import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    letters = [chr(ord('A') + i) for i in range(COLUMNS)]
    print('  ' + '   '.join(letters))
    # Print rows with separators
    for r in range(ROWS):
        print('+' + '---+' * COLUMNS)
        row_str = '|'
        for c in range(COLUMNS):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print('+' + '---+' * COLUMNS)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    if 0 <= col < COLUMNS:
        return True
    return False

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    # Find lowest empty row in column
    for row in range(ROWS -1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column full

def check_win(board, row, col, checker):
    # Directions to check: horizontal, vertical, diagonal /
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False

def board_full(board):
    for c in range(COLUMNS):
        if not is_column_full(board, c):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]

    # Choose random starting player
    current_player_index = random.randint(0, PLAYERS -1)
    print_board(board)

    while True:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        
        # Input loop
        while True:
            col_char = input(prompt).strip().upper()
            if not is_valid_column(col_char):
                continue
            col = ord(col_char) - ord('A')
            if is_column_full(board, col):
                # Player loses turn, so break input loop and go next player
                break
            else:
                break

        # If column full, lose turn
        if is_column_full(board, col):
            current_player_index = (current_player_index +1) % PLAYERS
            print_board(board)
            continue

        row = place_checker(board, col, checker)
        print_board(board)

        # Check win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Next player
        current_player_index = (current_player_index +1) % PLAYERS

if __name__ == '__main__':
    main()
