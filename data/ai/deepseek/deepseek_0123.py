import os
import random
from typing import List, Tuple

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board() -> List[List[str]]:
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board: List[List[str]]) -> None:
    """Print the game board with column labels and borders."""
    # Clear the screen before printing the board
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print the board
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+---' * BOARD_COLS + '+')

def get_valid_input(player: str) -> int:
    """
    Get a valid column input from the player.
    Returns the column index (0-based) or -1 if the column is full.
    """
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").strip().upper()
            if not col_input or len(col_input) != 1:
                print("Invalid input. Please enter a single letter from A to", chr(65 + BOARD_COLS - 1))
                continue
            
            col = ord(col_input) - ord('A')
            if col < 0 or col >= BOARD_COLS:
                print("Invalid column. Please enter a letter between A and", chr(65 + BOARD_COLS - 1))
                continue
            
            # Check if the column is full
            if board[0][col] != ' ':
                print("Column is full. Please choose another column.")
                return -1
            
            return col
        except KeyboardInterrupt:
            exit()
        except:
            print("Invalid input. Please enter a letter from A to", chr(65 + BOARD_COLS - 1))

def place_checker(board: List[List[str]], col: int, player: str) -> bool:
    """
    Place the player's checker in the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board: List[List[str]], player: str) -> bool:
    """
    Check if the player has won by getting 4 in a row (horizontal, vertical, or diagonal).
    """
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    
    return False

def is_draw(board: List[List[str]]) -> bool:
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main() -> None:
    """Main game loop."""
    global board
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_input(current_player)
        
        if col == -1:  # Column is full
            continue
        
        placed = place_checker(board, col, current_player)
        if not placed:
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
