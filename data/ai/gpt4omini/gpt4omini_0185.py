import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Players' checkers

def create_board():
    """Create the Connect 4 board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board to the terminal."""
    os.system('clear')  # Clear screen for a better view
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    """Check if the column input is valid."""
    return column in range(COLS)

def get_lowest_empty_row(board, col):
    """Return the lowest empty row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1  # Column is full

def check_win(board, player):
    """Check if the specified player has a winning combination."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    """Check if the board is full and there are no winners."""
    return all(board[row][col] != ' ' for row in range(ROWS) for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, 1)  # Randomly choose starting player
    players_count = 2  # Set for 2 players game
    current_player = PLAYERS[current_player_index]

    print_board(board)

    while True:
        # Prompt the current player to choose a column
        column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").strip().upper()
        
        # Validate input
        if len(column_input) != 1 or not column_input.isalpha():
            print("Invalid input! Please enter a column label (A-G).")
            continue
        
        column = ord(column_input) - 65  # Convert letter to index
        
        if not is_valid_input(column):
            print("Invalid column! Please enter a column between A and G.")
            continue

        # Place the checker
        row = get_lowest_empty_row(board, column)
        if row == -1:  # If the column is full
            print("Column full! Please choose another column.")
            continue
        
        board[row][column] = current_player
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % players_count
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    main()
