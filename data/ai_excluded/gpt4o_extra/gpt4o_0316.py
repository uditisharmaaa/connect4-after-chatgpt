import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
VALID_COLUMNS = [chr(i) for i in range(ord('A'), ord('A') + COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(VALID_COLUMNS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def select_first_player():
    return random.randint(0, PLAYER_COUNT - 1)

def is_valid_column(input_col):
    return input_col in VALID_COLUMNS

def get_next_open_row(board, col_index):
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == ' ':
            return r
    return None

def place_checker(board, col_index, checker):
    row = get_next_open_row(board, col_index)
    if row is not None:
        board[row][col_index] = checker
        return True
    return False

def check_win(board, checker):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonal
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonal
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    board = create_board(ROWS, COLS)
    current_player_index = select_first_player()
    
    print_board(board)
    
    while True:
        current_player_checker = CHECKERS[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        col_input = input().strip().upper()
        
        if is_valid_column(col_input):
            col_index = VALID_COLUMNS.index(col_input)

            if place_checker(board, col_index, current_player_checker):
                print_board(board)

                if check_win(board, current_player_checker):
                    print(f"Player {current_player_checker} won!")
                    break
                elif check_draw(board):
                    print("It's a draw!")
                    break

                current_player_index = (current_player_index + 1) % PLAYER_COUNT
            else:
                print("Column is full, you lose your turn.")
        else:
            print("Invalid input. Please enter a valid column (A-G).")

if __name__ == "__main__":
    play_game()
