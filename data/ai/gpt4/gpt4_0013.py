import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# Initialize the board
def create_board():
    return [[EMPTY_CELL for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Check valid column input
def is_valid_column(choice, board):
    if len(choice) != 1 or not choice.isalpha():
        return False
    col_index = ord(choice.upper()) - 65
    return 0 <= col_index < COLS and board[0][col_index] == EMPTY_CELL

# Drop checker into the selected column
def drop_checker(board, col_index, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == EMPTY_CELL:
            board[row][col_index] = symbol
            return row, col_index

# Check for a win in all directions
def check_win(board, row, col, symbol):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row, col
            while True:
                r += step * dr
                c += step * dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                    count += 1
                    if count == 4:
                        return True
                else:
                    break
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != EMPTY_CELL for col in range(COLS))

# Main game loop
def connect_four():
    board = create_board()
    num_players = 2
    symbols = PLAYER_SYMBOLS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    while True:
        print_board(board)
        print(f"Player {symbols[current_player]}, please enter a column:")
        choice = input().strip().upper()

        if not is_valid_column(choice, board):
            print("Invalid input. Try again.")
            continue

        col_index = ord(choice) - 65
        row, col = drop_checker(board, col_index, symbols[current_player])

        if check_win(board, row, col, symbols[current_player]):
            print_board(board)
            print(f"Player {symbols[current_player]} won!")
            break

        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    connect_four()
