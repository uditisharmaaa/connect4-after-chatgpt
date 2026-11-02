import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    os.system('clear')

def create_board():
    """Create a 2D board initialized with whitespace."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Row separator

def is_valid_input(column):
    """Check if the user input is a valid column."""
    return column in (chr(65 + i) for i in range(COLS))

def get_column_index(column):
    """Get the index of the column from the letter (A-G)."""
    return ord(column) - 65  # Convert from ASCII to index

def place_checker(board, column, checker):
    """Place the checker in the specified column."""
    col_idx = get_column_index(column)
    for row in reversed(board):  # Check from bottom to top
        if row[col_idx] == " ":
            row[col_idx] = checker
            return True  # Successfully placed checker
    return False  # Column is full

def check_win(board, checker):
    """Check the board for a win condition for the specified checker."""
    # Check horizontal, vertical and diagonal conditions
    for r in range(ROWS):
        for c in range(COLS):
            if (c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4))) or \
               (r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4))) or \
               (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4))) or \
               (r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def check_draw(board):
    """Check if the board is full and there are no more valid moves."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Main game function."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select first player

    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G): ", end="")
        
        while True:
            column = input().strip().upper()
            if is_valid_input(column):
                if place_checker(board, column, current_player):
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input. Please enter a valid column (A-G): ")
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
            
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
            
        current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player

if __name__ == "__main__":
    play_game()
