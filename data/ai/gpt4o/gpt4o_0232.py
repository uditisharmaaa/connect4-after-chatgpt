import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    headers = '  ' + '   '.join(chr(c) for c in range(65, 65 + COLS))
    print(headers)
    print('+---' * COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLS + '+')

def is_valid_input(column):
    return column.isalpha() and 65 <= ord(column.upper()) < 65 + COLS

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_for_win(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Positive diagonal check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Negative diagonal check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(board[r][c] != ' ' for r in range(ROWS) for c in range(COLS))

def connect4():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        column = input(f"Player {player_checker}, please enter a column: ")

        if is_valid_input(column):
            col_idx = ord(column.upper()) - 65
            row_idx = get_next_open_row(board, col_idx)

            if row_idx is not None:
                board[row_idx][col_idx] = player_checker
                print_board(board)

                if check_for_win(board, player_checker):
                    print(f"Player {player_checker} won!")
                    break
                elif is_draw(board):
                    print("The game is a draw!")
                    break

                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column is full. Please choose another.")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    connect4()
