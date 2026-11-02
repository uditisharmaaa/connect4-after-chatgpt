import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Symbols for up to 5 players

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the board boundaries and cells
    for row in board:
        print("+" + "---+".join([""] * (COLS + 1)))  # Border line
        print("|" + "|".join(f" {cell} " for cell in row) + "|")  # Cell content
        
    print("+" + "---+".join([""] * (COLS + 1)))  # Bottom border line

def is_valid_move(board, col):
    """Check if a move is valid (column not full and within bounds)."""
    return 0 <= col < COLS and board[0][col] == " "

def get_column_input(current_player):
    """Get and validate the column input from the current player."""
    while True:
        try:
            user_input = input(f"Player {current_player}, please enter a column: ").upper()
            if len(user_input) != 1:
                print("Please enter a single letter.")
                continue
            col = ord(user_input) - ord('A')
            if 0 <= col < COLS:
                return col
            else:
                print(f"Column must be between A and {chr(ord('A') + COLS - 1)}")
        except (ValueError, TypeError):
            print("Invalid input. Please enter a letter.")

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest empty row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full (should not reach here if move is validated)

def check_winner(board, row, col, checker):
    """Check if the last move resulted in a win (4 in a row)."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current checker is part of the line
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (no more moves possible)."""
    return all(cell != " " for cell in board[0])

def switch_player(current_player, players):
    """Switch to the next player in the list."""
    current_index = players.index(current_player)
    next_index = (current_index + 1) % len(players)
    return players[next_index]

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    print_board(board)
    
    while True:
        col = get_column_input(current_player)
        if not is_valid_move(board, col):
            print(f"Column {chr(65 + col)} is full. Try another column.")
            continue
        
        row = place_checker(board, col, current_player)
        print_board(board)
        
        if check_winner(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_board_full(board):
            print("Game is a draw!")
            break
        
        current_player = switch_player(current_player, players)

if __name__ == "__main__":
    main()
