import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]  # Ensure only required checkers are used

def create_board(rows, columns):
    """Create the game board with the specified dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column labels A, B, C, etc.
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_column(board):
    """Prompt player for a valid column input."""
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) == 1 and col_input.isalpha():
            col_index = ord(col_input) - 65  # Convert column letter to index
            if 0 <= col_index < len(board[0]) and board[0][col_index] == " ":
                return col_index
        print("Invalid input. Try again.")

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return

def check_win(board, checker):
    """Check if the current player has a winning configuration."""
    # Check horizontal, vertical and both diagonal directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == checker:
                for dr, dc in directions:
                    if check_direction(board, row, col, dr, dc, checker):
                        return True
    return False

def check_direction(board, row, col, dr, dc, checker):
    """Check 4 checkers in a specified direction for a win."""
    for i in range(4):
        r, c = row + i * dr, col + i * dc
        if not (0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker):
            return False
    return True

def check_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def play_game():
    """Play the Connect 4 game."""
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)  # Choose a random player to start
    print_board(board)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker},", end=" ")
        col = get_valid_column(board)
        place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to next player turn
        current_player_index = (current_player_index + 1) % PLAYERS

play_game()
