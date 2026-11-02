import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the board with all empty cells."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current board state."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print top border
    print("+" + "+".join(["---"] * cols) + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "+".join(["---"] * cols) + "+")


def is_valid_input(col_letter, cols):
    """Validate the column input."""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_letter = col_letter.upper()
    col_index = ord(col_letter) - ord('A')
    return 0 <= col_index < cols


def get_column_index(col_letter):
    """Convert column letter to index."""
    return ord(col_letter.upper()) - ord('A')


def can_place_checker(board, col_index, rows):
    """Check if a checker can be placed in the given column."""
    return board[0][col_index] == " "


def place_checker(board, col_index, checker, rows):
    """Place a checker in the given column and return the row index."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker, rows, cols):
    """Check if the last placed checker results in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def get_player_move(player_checker, cols):
    """Get a valid move from the current player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_input(user_input, cols):
            print("Invalid input. Please enter a valid column (A-" + chr(65 + cols - 1) + ").")
            continue
        
        return get_column_index(user_input)


def play_game(rows, cols, num_players):
    """Main game loop."""
    board = initialize_board(rows, cols)
    checkers = CHECKERS[:num_players]
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board, cols)
    
    while True:
        current_checker = checkers[current_player_index]
        
        # Get player move
        col_index = get_player_move(current_checker, cols)
        
        # Check if column is full
        if not can_place_checker(board, col_index, rows):
            print("Column is full. You lose this turn.")
            current_player_index = (current_player_index + 1) % num_players
            continue
        
        # Place checker and get row index
        row_index = place_checker(board, col_index, current_checker, rows)
        
        # Print updated board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row_index, col_index, current_checker, rows, cols):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, rows, cols):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players


def main():
    """Main function to start the game."""
    play_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
