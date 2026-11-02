import os
import random
from typing import List, Tuple

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First NUM_PLAYERS symbols

def initialize_board() -> List[List[str]]:
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board: List[List[str]]):
    """Print the current state of the board with column labels."""
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def is_valid_column(col: str) -> bool:
    """Check if the column input is valid (letter within board bounds)."""
    if len(col) != 1:
        return False
    col_idx = ord(col.upper()) - ord('A')
    return 0 <= col_idx < COLS

def get_column_index(col: str) -> int:
    """Convert column letter to 0-based index."""
    return ord(col.upper()) - ord('A')

def drop_checker(board: List[List[str]], col_idx: int, checker: str) -> bool:
    """Drop a checker into the specified column.
    Returns True if successful, False if column is full."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board: List[List[str]], row: int, col: int, checker: str) -> bool:
    """Check if the last move at (row, col) resulted in a win."""
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # the current position
        
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
        
        if count >= 4:
            return True
    
    return False

def is_draw(board: List[List[str]]) -> bool:
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    
    while True:
        player = PLAYERS[current_player_idx]
        print(f"Player {player}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A-" + chr(65 + COLS - 1) + ")")
            continue
        
        col_idx = get_column_index(col_input)
        if not drop_checker(board, col_idx, player):
            print("Column is full. You lose your turn.")
        else:
            clear_screen()
            print_board(board)
            
            if check_win(board, next((r for r in range(ROWS) if board[r][col_idx] == player), -1), col_idx, player):
                print(f"Player {player} won!")
                break
            
            if is_draw(board):
                print("Game ended in a draw!")
                break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
