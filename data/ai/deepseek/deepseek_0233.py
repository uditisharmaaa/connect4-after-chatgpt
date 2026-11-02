import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column letters
    print("\n  " + "   ".join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print("+" + "---+".join(["" for _ in range(COLS)]) + "+")
    
    for row in board:
        # Print row cells
        print("|" + "|".join([" " + cell + " " for cell in row]) + "|")
        # Print row border
        print("+" + "---+".join(["" for _ in range(COLS)]) + "+")

def get_player_turn(current_player, players):
    """Get the current player's turn."""
    return players[current_player]

def get_valid_column():
    """Ask the player for a column and validate the input."""
    while True:
        col = input(f"Player {current_checker}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha() or ord(col) < 65 or ord(col) >= 65 + COLS:
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
        else:
            return ord(col) - 65  # Convert letter to column index

def place_checker(board, col, checker):
    """Place the checker in the lowest empty row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column is full

def check_win(board, row, col, checker):
    """Check if the last move caused a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # If 4 in a row, return True
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    global current_checker
    
    # Initialize game
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.randint(0, PLAYERS - 1)
    current_checker = players[current_player]
    
    os.system('clear')
    print("Starting Connect 4!")
    print(f"Player {current_checker} goes first.")
    print_board(board)
    
    while True:
        # Get valid column from player
        col = get_valid_column()
        
        # Place checker
        result = place_checker(board, col, current_checker)
        if result is None:
            print("Column is full. Try another column.")
            continue
        
        row, _ = result
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch players
        current_player = (current_player + 1) % PLAYERS
        current_checker = players[current_player]

if __name__ == "__main__":
    main()
