import os
import random

# Constants for the board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def create_board():
    """Creates a new game board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

def is_valid_input(column, board):
    """Checks if the input column is valid and not full."""
    if column < 0 or column >= COLS:
        return False  # Out of bounds
    if board[0][column] != ' ':
        return False  # Column is full
    return True

def drop_checker(board, column, checker):
    """Drops a checker into the specified column."""
    for row in reversed(board):  # Start from the bottom row
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # This should never happen if is_valid_input is checked

def check_win(board, checker):
    """Checks for a win condition for the specified checker."""
    # Check horizontal, vertical, and diagonal wins
    for r in range(ROWS):
        for c in range(COLS):
            if (check_horizontal(board, r, c, checker) or
                check_vertical(board, r, c, checker) or
                check_diagonal(board, r, c, checker)):
                return True
    return False

def check_horizontal(board, r, c, checker):
    """Checks for horizontal win starting from (r, c)."""
    if c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)):
        return True
    return False

def check_vertical(board, r, c, checker):
    """Checks for vertical win starting from (r, c)."""
    if r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)):
        return True
    return False

def check_diagonal(board, r, c, checker):
    """Checks for diagonal wins starting from (r, c)."""
    # Check \ direction
    if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)):
        return True
    # Check / direction
    if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == checker for i in range(4)):
        return True
    return False

def check_draw(board):
    """Checks if the board is full and there is no winner."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    print_board(board)
    
    while True:
        player_index = PLAYERS.index(current_player)
        print(f"Player {current_player}, please enter a column (A-G): ", end="")
        
        while True:
            try:
                column_input = input().strip().upper()
                if column_input not in [chr(65 + i) for i in range(COLS)]:  # Check valid letter
                    raise ValueError("Invalid input. Please enter a letter (A-G).")
                column = ord(column_input) - 65  # Convert letter to column index
                if not is_valid_input(column, board):
                    print("Column is full or invalid. Please try again.")
                    continue
                break
            except ValueError as e:
                print(e)
        
        drop_checker(board, column, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = PLAYERS[(player_index + 1) % len(PLAYERS)]  # Switch to the next player

if __name__ == "__main__":
    main()
