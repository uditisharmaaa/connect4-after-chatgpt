import os
import random

# Constants for game settings
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a new game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the console
    print("  " + "   ".join(chr(65 + c) for c in range(COLS)))
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column():
    """Prompt the user for a valid column input and return its index."""
    while True:
        column = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").strip().upper()
        if len(column) == 1 and column >= 'A' and column < chr(65 + COLS):
            return ord(column) - 65
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, player):
    """Place a check in the board for player at the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = player
            return True
    return False

def check_winner(board, player):
    """Check all possible win conditions for the current player."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if check_directions(board, r, c, player):
                    return True
    return False

def check_directions(board, row, col, player):
    """Check all four directions for a win."""
    return (check_direction(board, row, col, player, 1, 0) or  # Horizontal
            check_direction(board, row, col, player, 0, 1) or  # Vertical
            check_direction(board, row, col, player, 1, 1) or  # Diagonal /
            check_direction(board, row, col, player, 1, -1)    # Diagonal \
           )

def check_direction(board, row, col, player, delta_row, delta_col):
    """Check a single direction for a win."""
    count = 0
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    """Check if the board is full and there is no winner."""
    for row in board:
        if ' ' in row:
            return False
    return True

# Main game loop
if __name__ == "__main__":
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        
        # Get the current player based on index
        current_player = PLAYERS[current_player_index]
        
        # Get valid column from player
        col = get_valid_column()

        # Place checker, if possible
        if place_checker(board, col, current_player):
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            # Move to the next player
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Choose another column.")
