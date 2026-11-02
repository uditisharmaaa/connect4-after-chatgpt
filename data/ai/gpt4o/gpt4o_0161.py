import os
import random

# Constants
NUM_PLAYERS = 2
BOARD_ROWS = 6
BOARD_COLUMNS = 7
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def create_board():
    return [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(BOARD_COLUMNS)))
    print("+---" * BOARD_COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * BOARD_COLUMNS + "+")

def is_valid_column(column, board):
    return column.isalpha() and ord(column.upper()) - ord('A') < BOARD_COLUMNS

def get_next_open_row(board, col_index):
    for row in reversed(board):
        if row[col_index] == " ":
            return board.index(row)
    return None

def check_for_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(BOARD_COLUMNS - 3):
            if row[col] == checker and row[col+1] == checker and row[col+2] == checker and row[col+3] == checker:
                return True
    # Check vertical
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Check positive diagonal (/)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Check negative diagonal (\)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def check_for_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = create_board()
    print_board(board)
    game_over = False
    current_player = random.choice(range(NUM_PLAYERS))

    while not game_over:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        player_input = input().strip().upper()

        if not is_valid_column(player_input, board):
            print("Invalid column. Please enter a column label (letters A-G).")
            continue
        
        col_index = ord(player_input) - ord('A')
        row = get_next_open_row(board, col_index)

        if row is None:
            print("Column full. Turn lost.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        board[row][col_index] = CHECKERS[current_player]
        print_board(board)

        if check_for_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        elif check_for_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
