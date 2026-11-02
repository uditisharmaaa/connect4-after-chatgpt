import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
NUM_PLAYERS = 2  # Can be set to 2-5 players

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # Column letters
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, cols):
    if len(column) != 1 or not column.isalpha():
        return False
    idx = ord(column.upper()) - 65
    return 0 <= idx < cols

def is_column_full(board, col_idx):
    return board[0][col_idx] != " "

def drop_checker(board, col_idx, checker):
    for row in range(ROWS - 1, -1, -1):  # Start from bottom row
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            break

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))  # Top row full

def main():
    # Initialize board and game variables
    board = create_board(ROWS, COLS)
    player_order = random.sample(PLAYERS[:NUM_PLAYERS], NUM_PLAYERS)
    current_player_idx = 0
    clear_screen()
    print_board(board)

    while True:
        current_player = player_order[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()
        
        # Validate input
        if not is_valid_column(user_input, COLS):
            print("Invalid column. Try again.")
            continue

        col_idx = ord(user_input) - 65  # Convert column letter to index
        if is_column_full(board, col_idx):
            print("Column is full. Try again.")
            continue

        # Place the checker
        drop_checker(board, col_idx, current_player)
        clear_screen()
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
