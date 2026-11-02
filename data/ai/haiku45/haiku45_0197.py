import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")


def get_column_input(board, player_checker):
    """Get and validate column input from player."""
    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            
            if len(col_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            col = ord(col_input) - ord('A')
            
            if col < 0 or col >= COLS:
                print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
                continue
            
            if board[0][col] != " ":
                print("Column is full. Please choose another column.")
                continue
            
            return col
        except:
            print("Invalid input. Please enter a valid column letter.")


def place_checker(board, col, checker):
    """Place checker in the lowest available position in the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, row, col, checker):
    """Check if the last placed checker results in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLS))


def play_game():
    """Main game loop."""
    board = initialize_board()
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {checkers[current_player]} starts!")
    
    while True:
        col = get_column_input(board, checkers[current_player])
        
        # Find the row where the checker will be placed
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == " ":
                board[row][col] = checkers[current_player]
                print_board(board)
                
                # Check for win
                if check_win(board, row, col, checkers[current_player]):
                    print(f"Player {checkers[current_player]} won!")
                    return
                
                # Check for draw
                if is_board_full(board):
                    print("It's a draw!")
                    return
                
                # Move to next player
                current_player = (current_player + 1) % NUM_PLAYERS
                break


if __name__ == "__main__":
    play_game()
