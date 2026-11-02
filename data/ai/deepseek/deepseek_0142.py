import os
import random

# Constants
COLUMNS = 7
ROWS = 6
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize an empty board with ROWS rows and COLUMNS columns."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    
    # Print each row with borders
    border = "+" + ("---+" * COLUMNS)
    print(border)
    for row in board:
        row_str = "| " + " | ".join(f" {cell} " if cell != " " else " " for cell in row) + " |"
        print("|" + "|".join(f" {cell} " if cell != " " else "   " for cell in row) + "|")
        print(border)

def get_valid_move(board, current_player):
    """Prompt the player for a valid column."""
    while True:
        move = input(f"Player {current_player}, please enter a column: ").upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-Z).")
            continue
        col = ord(move) - ord('A')
        if col < 0 or col >= COLUMNS:
            print(f"Column must be between A and {chr(65 + COLUMNS - 1)}.")
            continue
        if board[0][col] != " ":
            print("That column is full. Please choose another.")
            continue
        return col

def place_checker(board, col, symbol):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],   # Vertical
        [(1, 1), (-1, -1)],  # Diagonal down-right
        [(1, -1), (-1, 1)]   # Diagonal down-left
    ]
    
    for direction_pair in directions:
        total = 1  # Includes the current checker
        
        for dr, dc in direction_pair:
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
                total += 1
                r += dr
                c += dc
        
        if total >= 4:
            return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for cell in board[0])

def play_game():
    """Main game loop."""
    board = initialize_board()
    players = PLAYER_SYMBOLS[:PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        col = get_valid_move(board, current_player)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    play_game()
