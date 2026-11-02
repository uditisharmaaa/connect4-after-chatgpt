import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    """Clears the console."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns an empty game board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    # Print column headers (A-G, etc.)
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+" + "---+" * len(board[0]))
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    """Checks if the column input is valid and not full."""
    if len(column) != 1 or not column.isalpha() or not column.isupper():
        return False
    col_index = ord(column) - 65  # Convert letter to index
    return 0 <= col_index < len(board[0]) and board[0][col_index] == " "

def get_next_open_row(board, col_index):
    """Returns the index of the next available row in the column."""
    for row in reversed(board):
        if row[col_index] == " ":
            return board.index(row)
    return -1  # Column is full

def drop_checker(board, row, col, checker):
    """Drops a checker into the given position."""
    board[row][col] = checker

def check_win(board, checker):
    """Checks for a winning condition."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal locations
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical locations
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def get_player_input(player, board):
    """Prompts the player for input and validates it."""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if is_valid_column(column, board):
            col_index = ord(column) - 65
            return col_index
        print("Invalid input. Please try again.")

def play_game():
    """Main game logic."""
    # Initialize board and players
    num_players = 2  # Default number of players for the assignment
    board = create_board(ROWS, COLS)
    player_symbols = PLAYER_SYMBOLS[:num_players]
    random.shuffle(player_symbols)
    
    # Choose starting player randomly
    current_player = 0
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        col_index = get_player_input(player_symbols[current_player], board)
        row_index = get_next_open_row(board, col_index)
        
        if row_index == -1:
            print(f"Column {chr(65 + col_index)} is full! You lose your turn.")
        else:
            drop_checker(board, row_index, col_index, player_symbols[current_player])
            print_board(board)

            # Check win condition
            if check_win(board, player_symbols[current_player]):
                print(f"Player {player_symbols[current_player]} won!")
                break

            # Check draw condition
            if check_draw(board):
                print("The game is a draw!")
                break

            # Switch to the next player
            current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game()
