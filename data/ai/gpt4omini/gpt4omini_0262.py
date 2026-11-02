import os
import random

# Constants for board dimensions and player checkers
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Creates a game board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the screen for a fresh display
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels
    print("+" + "---+" * COLUMNS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLUMNS)  # Row border

def is_valid_input(column):
    """Checks if the input is a valid column."""
    if len(column) != 1 or not column.isalpha():
        return False
    column_index = ord(column.upper()) - 65
    return 0 <= column_index < COLUMNS

def get_empty_row(board, column_index):
    """Returns the lowest empty row index in the specified column, -1 if full."""
    for row in reversed(range(ROWS)):
        if board[row][column_index] == ' ':
            return row
    return -1  # Column is full

def check_win(board, player):
    """Checks if the given player has won the game."""
    # Check horizontal, vertical, and diagonal for wins
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                if check_direction(board, row, col, player, 1, 0) or \
                   check_direction(board, row, col, player, 0, 1) or \
                   check_direction(board, row, col, player, 1, 1) or \
                   check_direction(board, row, col, player, 1, -1):
                    return True
    return False

def check_direction(board, row, col, player, delta_row, delta_col):
    """Checks for 4 consecutive checkers in a specific direction."""
    count = 0
    for step in range(4):
        r = row + step * delta_row
        c = col + step * delta_col
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    """Checks if the board is full."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select starting player
    
    while True:
        print_board(board)
        current_player = PLAYERS[current_player_index]
        column_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()

        # Validate user input
        while not is_valid_input(column_input):
            column_input = input(f"Invalid input. Player {current_player}, please enter a valid column (A-G): ").upper()
        
        column_index = ord(column_input) - 65  # Convert letter to index
        empty_row = get_empty_row(board, column_index)

        if empty_row == -1:
            print("Column is full. Try again.")
            continue  # Player skips their turn

        # Place the checker
        board[empty_row][column_index] = current_player
        
        # Check for a win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch players
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
