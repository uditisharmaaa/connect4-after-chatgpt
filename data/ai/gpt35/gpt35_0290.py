import os
import random

# Constants for the game configuration
ROWS = 6        # Number of rows in the board
COLUMNS = 7     # Number of columns in the board (max 26 supported)
PLAYERS = 2     # Number of players (between 2 and 5)
WIN_LENGTH = 4  # Number of checkers in a row needed to win

# Checkers for players (fixed order)
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """
    Create a game board with given rows and columns.
    Board cells are initialized with a space character.
    Returns a 2D list representing the board.
    """
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """
    Print the current game board with column labels A..G and cell separators.
    Rows have no labels.
    """
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers (A, B, C, ...)
    headers = "  "
    for col in range(columns):
        headers += "  " + chr(ord('A') + col) + " "
    print(headers)
    
    # Print board with row separators
    separator = "+" + "---+" * columns
    for r in range(rows):
        print(separator)
        row_str = "|"
        for c in range(columns):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(separator)

def is_valid_column(col_letter, columns):
    """
    Check if the given column letter is valid for the board.
    """
    if len(col_letter) != 1:
        return False
    if not ('A' <= col_letter <= chr(ord('A') + columns - 1)):
        return False
    return True

def get_column_index(col_letter):
    """
    Convert uppercase column letter to zero-based column index.
    """
    return ord(col_letter) - ord('A')

def place_checker(board, col_idx, checker):
    """
    Place the checker in the lowest available row in the specified column.
    If the column is full, return False.
    Otherwise, place the checker and return True.
    """
    rows = len(board)
    # Start checking from bottom row upwards
    for row in reversed(range(rows)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    """
    Check if the given checker has won by forming four in a row.
    Checks horizontal, vertical, and two diagonal directions.
    Returns True if win detected, False otherwise.
    """
    rows = len(board)
    columns = len(board[0])
    
    # Helper function to check 4 in a row starting at (r,c) in direction (dr, dc)
    def check_direction(r, c, dr, dc):
        for i in range(WIN_LENGTH):
            nr, nc = r + dr*i, c + dc*i
            if nr < 0 or nr >= rows or nc < 0 or nc >= columns:
                return False
            if board[nr][nc] != checker:
                return False
        return True
    
    for r in range(rows):
        for c in range(columns):
            if board[r][c] == checker:
                # Check horizontal right
                if c + WIN_LENGTH <= columns and check_direction(r, c, 0, 1):
                    return True
                # Check vertical down
                if r + WIN_LENGTH <= rows and check_direction(r, c, 1, 0):
                    return True
                # Check diagonal down-right
                if r + WIN_LENGTH <= rows and c + WIN_LENGTH <= columns and check_direction(r, c, 1, 1):
                    return True
                # Check diagonal down-left
                if r + WIN_LENGTH <= rows and c - WIN_LENGTH + 1 >= 0 and check_direction(r, c, 1, -1):
                    return True
    return False

def check_draw(board):
    """
    Check if the board is full: no empty spaces remain.
    Returns True if draw, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Initialize board and game variables
    board = create_board(ROWS, COLUMNS)
    
    # Limit number of players between 2 and 5
    num_players = PLAYERS
    if num_players < 2:
        num_players = 2
    elif num_players > 5:
        num_players = 5
    
    players = CHECKERS[:num_players]
    
    # Randomly select first player index
    current_player_idx = random.randint(0, num_players - 1)
    
    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        
        # Get valid input from player (uppercase letter A..G)
        while True:
            col_input = input(prompt).strip().upper()
            if not is_valid_column(col_input, COLUMNS):
                # Invalid input - not a proper column
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_idx = get_column_index(col_input)
            # Attempt to place checker
            placed = place_checker(board, col_idx, current_checker)
            if not placed:
                # Column full, lose turn without placement (as per spec)
                # Inform player and break input loop to proceed to next player
                # Note: The instructions specify the player loses turn if column full
                # so no retry here.
                print("Column is full! You lose your turn.")
                break
            else:
                # Successfully placed checker
                break
        
        # If checker was placed, check for a win
        if placed:
            if check_win(board, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                return
            elif check_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                return
        
        # Move to next player in round robin fashion
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
