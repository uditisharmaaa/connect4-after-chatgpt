import os
import random
from typing import List, Tuple

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:PLAYERS]

def initialize_board() -> List[List[str]]:
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def print_board(board: List[List[str]]):
    """Print the game board with column labels."""
    # Print column letters
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def get_valid_column(board: List[List[str]], player: str) -> int:
    """Get a valid column input from the player."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            if len(col_input) != 1 or not col_input.isalpha():
                print("Please enter a single letter.")
                continue
            col = ord(col_input) - ord('A')
            if col < 0 or col >= COLS:
                print(f"Column must be between A and {chr(65 + COLS - 1)}.")
                continue
            if board[0][col] != " ":
                print("Column is full. Choose another column.")
                continue
            return col
        except KeyboardInterrupt:
            print("\nGame terminated.")
            exit()
        except:
            print("Invalid input. Please try again.")

def place_checker(board: List[List[str]], col: int, player: str) -> Tuple[int, int]:
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return (row, col)
    return (-1, -1)  # Should never reach here if column is validated first

def check_win(board: List[List[str]], row: int, col: int, player: str) -> bool:
    """Check if the player has won after placing a checker at (row, col)."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1), # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in one direction
        for step in range(1, 4):
            r, c = row + step * dr, col + step * dc
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        # Check in the opposite direction
        for step in range(1, 4):
            r, c = row - step * dr, col - step * dc
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for cell in board[0])

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(PLAYERS))
    
    while True:
        clear_screen()
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        col = get_valid_column(board, player_symbol)
        row, col = place_checker(board, col, player_symbol)
        
        if check_win(board, row, col, player_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbol} won!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
