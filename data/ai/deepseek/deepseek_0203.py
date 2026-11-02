import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Create an empty board with ROWS x COLUMNS dimensions."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    
    # Print each row with borders
    for row in board:
        border = "+" + ("---+" * COLUMNS)
        row_str = "| " + " | ".join(cell for cell in row) + " |"
        print(border)
        print(row_str)
    
    print("+" + ("---+" * COLUMNS))

def is_valid_move(board, column):
    """Check if a move is valid (column exists and has space)."""
    return 0 <= column < COLUMNS and board[0][column] == " "

def place_checker(board, column, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won (4 in a row in any direction)."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 0
                    r, c = row, col
                    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
                        count += 1
                        if count == 4:
                            return True
                        r += dr
                        c += dc
    return False

def is_board_full(board):
    """Check if the board is completely filled."""
    return all(cell != " " for row in board for cell in row)

def get_column_input(player):
    """Get and validate column input from the player."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            if len(col_input) != 1 or not col_input.isalpha():
                print("Invalid input. Please enter a single letter (A-" + chr(65 + COLUMNS - 1) + ").")
                continue
            
            column = ord(col_input) - ord('A')
            if 0 <= column < COLUMNS:
                return column
            else:
                print(f"Column must be between A and {chr(65 + COLUMNS - 1)}.")
        except (ValueError, IndexError):
            print("Invalid input. Please try again.")

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        column = get_column_input(current_player)
        if not is_valid_move(board, column):
            print("Column is full. Please choose another column.")
            continue
        
        place_checker(board, column, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
