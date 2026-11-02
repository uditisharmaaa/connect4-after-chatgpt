import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Column headers
    headers = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS))
    print(headers)
    # Print rows from top to bottom
    for row in range(ROWS):
        print('+' + '---+' * COLS)
        row_str = '|'
        for col in range(COLS):
            row_str += ' ' + board[row][col] + ' |'
        print(row_str)
    print('+' + '---+' * COLS)

def is_valid_column(col_letter):
    if len(col_letter) != 1:
        return False
    col = ord(col_letter) - ord('A')
    return 0 <= col < COLS

def get_column_index(col_letter):
    return ord(col_letter) - ord('A')

def column_has_space(board, col):
    # Check if top row in this col is empty (means space exists below)
    return board[0][col] == ' '

def place_checker(board, col, checker):
    # Place checker in lowest available row in column col
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == checker:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, checker):
    # Check all four directions for 4 in a row

    # Horizontal
    left = check_direction(board, row, col - 1, 0, -1, checker)
    right = check_direction(board, row, col + 1, 0, 1, checker)
    if left + 1 + right >= WIN_CONDITION:
        return True

    # Vertical
    down = check_direction(board, row + 1, col, 1, 0, checker)
    # up not needed since checkers fall from top
    if 1 + down >= WIN_CONDITION:
        return True

    # Diagonal /
    up_left = check_direction(board, row - 1, col - 1, -1, -1, checker)
    down_right = check_direction(board, row + 1, col + 1, 1, 1, checker)
    if up_left + 1 + down_right >= WIN_CONDITION:
        return True

    # Diagonal \
    up_right = check_direction(board, row - 1, col + 1, -1, 1, checker)
    down_left = check_direction(board, row + 1, col - 1, 1, -1, checker)
    if up_right + 1 + down_left >= WIN_CONDITION:
        return True

    return False

def full_board(board):
    for col in range(COLS):
        if column_has_space(board, col):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, please enter a column:")

        # Input validation loop
        while True:
            choice = input().strip().upper()
            if not is_valid_column(choice):
                print("Invalid column. Please enter a valid column letter:")
                continue
            col = get_column_index(choice)
            if not column_has_space(board, col):
                # Column full, player loses turn
                print("Column is full. You lose your turn.")
                col = None
            break

        if col is not None:
            pos = place_checker(board, col, current_checker)
            print_board(board)
            if pos is None:
                # This should not happen since we checked column_has_space
                pass
            else:
                row, col_placed = pos
                if check_win(board, row, col_placed, current_checker):
                    print(f"Player {current_checker} won!")
                    break
                if full_board(board):
                    print("The game is a draw!")
                    break
        else:
            print_board(board)

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
