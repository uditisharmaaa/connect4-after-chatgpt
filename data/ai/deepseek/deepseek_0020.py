import os
import random
from typing import List, Tuple

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players

def initialize_board() -> List[List[str]]:
    """Create and return an empty game board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board: List[List[str]]) -> None:
    """Print the current state of the game board with column labels."""
    # Print column headers (A, B, C, ...)
    print(' ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows with borders
    border = '+' + ('---+' * COLS)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def get_valid_move(player_symbol: str, board: List[List[str]]) -> int:
    """
    Prompt the player for a valid column input and return the column index (0-based).
    Handles input validation and column availability.
    """
    while True:
        try:
            move = input(f"Player {player_symbol}, please enter a column: ").upper()
            if len(move) != 1 or not move.isalpha():
                print("Please enter a single letter (A-G).")
                continue
            
            col = ord(move) - ord('A')
            if col < 0 or col >= COLS:
                print(f"Please enter a letter between A and {chr(65 + COLS - 1)}.")
                continue
            
            if board[0][col] != ' ':
                print("That column is full. Please choose another.")
                continue
                
            return col
        except EOFError:
            print("\nInvalid input. Please try again.")
            continue

def place_piece(board: List[List[str]], col: int, player_symbol: str) -> int:
    """
    Place the player's piece in the specified column.
    Returns the row where the piece was placed.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row
    return -1  # Shouldn't happen if input is validated

def check_win(board: List[List[str]], row: int, col: int, player_symbol: str) -> bool:
    """
    Check if the last placed piece resulted in a win.
    Returns True if the player has won, False otherwise.
    """
    # Directions: horizontal, vertical, diagonal down-right, diagonal down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current piece
        
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def check_draw(board: List[List[str]]) -> bool:
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for cell in board[0])

def main() -> None:
    """Main game loop."""
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        clear_screen()
        print_board(board)
        
        col = get_valid_move(current_player, board)
        row = place_piece(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
