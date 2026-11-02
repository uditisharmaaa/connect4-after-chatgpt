import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Support for up to 5 players
COLUMN_LETTERS = [chr(c) for c in range(65, 65 + COLUMNS)]  # A, B, C, ...

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LETTERS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def is_valid_column(column):
    """Check if a column input is valid."""
    return column in COLUMN_LETTERS

def get_column_index(column):
    """Convert column letter to index."""
    return COLUMN_LETTERS.index(column)

def is_column_full(board, col_index):
    """Check if a column is full."""
    return all(board[row][col_index] != ' ' for row in range(ROWS))

def drop_checker(board, col_index, checker):
    """Drops the checker to the lowest available row in the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row, col_index

def check_winner(board, row, col, checker):
    """Check if placing a checker at (row, col) wins the game."""
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(-1, 0), (1, 0)],  # Vertical
        [(-1, -1), (1, 1)],  # Diagonal left-to-right
        [(-1, 1), (1, -1)]   # Diagonal right-to-left
    ]
    for direction in directions:
        count = 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Checks if the board is completely filled."""
    return all(is_column_full(board, col_index) for col_index in range(COLUMNS))

def main():
    # Initialize game
    board = create_board()
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player_index = random.randint(0, PLAYERS - 1)

    # Main game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        column = input("Please enter a column: ").strip().upper()

        # Validate user input
        if not is_valid_column(column):
            print("Invalid column. Choose a valid column (A-G).")
            continue

        col_index = get_column_index(column)
        if is_column_full(board, col_index):
            print(f"Column {column} is full. Choose a different column.")
            continue

        # Drop the checker and check game state
        row, col = drop_checker(board, col_index, players[current_player_index])
        if check_winner(board, row, col, players[current_player_index]):
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
