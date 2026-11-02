import os
import random

# Game constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system("clear")
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if a move is valid (column exists and has space)."""
    return 0 <= col < COLS and board[0][col] == " "


def place_checker(board, col, symbol):
    """Place a checker in the specified column, returns the row or -1 if invalid."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal \
        (1, -1)   # Diagonal /
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLS))


def get_player_input(player_symbol):
    """Get and validate player input for column selection."""
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord("A")
        
        if col >= COLS or col < 0:
            print(f"Invalid input. Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Random player selected: {players[current_player_idx]}\n")
    
    while True:
        # Get player input
        col = get_player_input(players[current_player_idx])
        
        # Place checker
        row = place_checker(board, col, players[current_player_idx])
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, players[current_player_idx]):
            print(f"Player {players[current_player_idx]} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
