import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a game board initialized with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clears the console
    print("  " + "   ".join([chr(i) for i in range(65, 65 + COLS)]))  # Column labels
    print("+" + "---+" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(col_str):
    """Check if input is a valid column letter."""
    return col_str.isalpha() and len(col_str) == 1 and 'A' <= col_str <= chr(65 + COLS - 1)

def get_column_index(col_str):
    """Convert column letter to index."""
    return ord(col_str) - 65

def drop_checker(board, col, player):
    """Place the checker in the specified column."""
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check for a win condition."""
    # Check horizontal, vertical, and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and all(board[row][col + i] == player for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == player for i in range(4))) or \
               (col + 3 < COLS and row + 3 < ROWS and all(board[row + i][col + i] == player for i in range(4))) or \
               (col - 3 >= 0 and row + 3 < ROWS and all(board[row + i][col - i] == player for i in range(4))):
                return True
    return False

def check_draw(board):
    """Check if the board is full."""
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        while not is_valid_input(col_input):
            print("Invalid input. Please enter a valid column (A-G).")
            col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()

        col_index = get_column_index(col_input)
        
        if drop_checker(board, col_index, current_player):
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
