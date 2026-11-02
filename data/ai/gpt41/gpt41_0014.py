import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26  # For extending the board size if needed
PLAYERS = 2    # Change to 2-5 as needed

CHECKER_SYMBOLS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows, 'clear' for Unix/Linux/Mac

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    # Print column headers
    print("  ", end="")
    for c in range(cols):
        print(f" {chr(ord('A') + c)}  ", end="")
    print()
    # Print separator
    print("+" + "---+" * cols)
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * cols)

def get_player_symbols(num_players):
    return CHECKER_SYMBOLS[:num_players]

def get_valid_input(prompt, valid_columns):
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and user_input in valid_columns:
            return user_input
        else:
            print(f"Invalid input. Please enter a valid column: {', '.join(valid_columns)}")

def insert_checker(board, col, checker):
    # Insert from bottom up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column full

def is_full(board):
    # If no cell is " ", board is full
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # include current checker
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def main():
    # Set up
    board = create_board(ROWS, COLS)
    player_symbols = get_player_symbols(PLAYERS)
    valid_columns = [chr(ord('A') + i) for i in range(COLS)]

    # Randomly choose first player
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board, COLS)
        checker = player_symbols[current_player]
        print(f"Player {checker}, please enter a column:")
        col_char = get_valid_input("> ", valid_columns)
        col = ord(col_char) - ord('A')
        # Try to insert checker
        inserted_row = insert_checker(board, col, checker)
        if inserted_row == -1:
            print(f"Column {col_char} is full. You lose your turn.")
        else:
            # Check for win
            if check_win(board, inserted_row, col, checker):
                clear_screen()
                print_board(board, COLS)
                print(f"Player {checker} won!")
                break
            # Check for draw
            if is_full(board):
                clear_screen()
                print_board(board, COLS)
                print("It's a draw!")
                break
        # Next player's turn (even if current move was invalid)
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
