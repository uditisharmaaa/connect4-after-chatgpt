import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the console screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create and initialize an empty board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board."""
    column_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(column_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, columns):
    """Check if the input column letter is valid."""
    return column.isalpha() and len(column) == 1 and 'A' <= column < chr(ord('A') + columns)

def find_row(board, column_index):
    """Find the lowest available row in the given column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][column_index] == " ":
            return row
    return -1  # Column is full

def player_won(board, player_token, row, col):
    """Check if the given player has won after their turn."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Right, Down, Diagonal Right, Diagonal Left
    for dr, dc in directions:
        count = 1
        for step in range(1, 4):
            r, c = row + dr * step, col + dc * step
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_token:
                count += 1
            else:
                break
        for step in range(1, 4):
            r, c = row - dr * step, col - dc * step
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_token:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is in a draw state (no empty spaces)."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    num_players = min(2, MAX_PLAYERS)  # Set to 2 as per assignment requirement
    player_tokens = PLAYER_TOKENS[:num_players]

    # Randomly choose the first player
    current_player = random.randint(0, num_players - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {player_tokens[current_player]}, it's your turn!")

        # Input validation loop
        while True:
            column_input = input("Please enter a column (A-G): ").strip().upper()
            if not is_valid_column(column_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            column_index = ord(column_input) - ord('A')
            row_index = find_row(board, column_index)
            if row_index == -1:
                print("Column is full. Please choose another column.")
                continue
            break

        # Place the checker
        board[row_index][column_index] = player_tokens[current_player]

        # Check for a win or draw
        if player_won(board, player_tokens[current_player], row_index, column_index):
            clear_screen()
            print_board(board)
            print(f"Player {player_tokens[current_player]} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
