import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLS)]  # ['A', 'B', 'C', ...]

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty board with specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_column_index(column_choice):
    """Converts a column letter to an index. Returns None if invalid."""
    if column_choice in COLUMN_LABELS:
        return COLUMN_LABELS.index(column_choice)
    return None

def drop_checker(board, col_idx, token):
    """Drops a checker into the specified column."""
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = token
            return True
    return False  # Column is full

def is_winning_move(board, token):
    """Checks if the board contains a winning line of 4 for the given token."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == token for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == token for i in range(4)):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == token for i in range(4)):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == token for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is full (draw condition)."""
    return all(cell != " " for row in board for cell in row)

def get_player_input(board, player_token):
    """Gets valid column input from the player."""
    while True:
        column_choice = input(f"Player {player_token}, please enter a column: ").strip().upper()
        col_idx = get_column_index(column_choice)
        if col_idx is not None and board[0][col_idx] == " ":
            return col_idx
        print("Invalid input, please try again.")

def main():
    """Main function to run the Connect 4 game."""
    # Initialize board and players
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print(f"Randomly chosen starting player: Player {PLAYER_TOKENS[current_player_idx]}")

    while True:
        print_board(board)
        
        # Get current player's move
        current_token = PLAYER_TOKENS[current_player_idx]
        col_idx = get_player_input(board, current_token)
        
        # Place the token
        drop_checker(board, col_idx, current_token)
        
        # Check for a win
        if is_winning_move(board, current_token):
            print_board(board)
            print(f"Player {current_token} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
