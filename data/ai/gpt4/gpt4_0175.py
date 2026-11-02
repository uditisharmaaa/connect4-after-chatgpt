import os
import random

# Constants for the game
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
TOTAL_PLAYERS = 2  # Default to 2 players; change for more players

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates an empty Connect 4 board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board."""
    clear_screen()
    # Print column labels
    col_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(col_labels)
    print("+" + "---+" * len(board[0]))
    # Print rows with contents
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_input(input_str, cols):
    """Checks if the input is a valid column letter."""
    return len(input_str) == 1 and input_str.isalpha() and 'A' <= input_str <= chr(65 + cols - 1)

def drop_checker(board, column, checker):
    """Drops a checker into the specified column."""
    for row in reversed(board):  # Start from the bottom
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    """Checks for a win condition."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Checks if the board is completely filled (draw)."""
    return all(cell != " " for row in board for cell in row)

def get_column_index(input_str):
    """Gets the zero-based column index from input string."""
    return ord(input_str.upper()) - 65

def main():
    # Initialize game variables
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:TOTAL_PLAYERS]
    current_player_idx = random.randint(0, TOTAL_PLAYERS - 1)
    
    while True:
        # Print the board and ask for input
        print_board(board)
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        player_input = input().strip().upper()
        
        # Validate input
        if not is_valid_input(player_input, COLS):
            print("Invalid input! Please enter a valid column letter.")
            continue
        
        column = get_column_index(player_input)
        if not drop_checker(board, column, current_player):
            print("Column is full! Try a different column.")
            continue
        
        # Check for winner or draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % TOTAL_PLAYERS

if __name__ == "__main__":
    main()
