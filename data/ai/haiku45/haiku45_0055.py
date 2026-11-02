import os
import random

# Constants
COLUMNS = 7
ROWS = 6
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    header = "  "
    for col in range(cols):
        header += chr(ord('A') + col) + "   "
    print(header)
    
    # Print board with borders
    for row in board:
        # Print top border
        border = "+"
        for _ in range(cols):
            border += "---+"
        print(border)
        
        # Print row content
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    
    # Print bottom border
    border = "+"
    for _ in range(cols):
        border += "---+"
    print(border)

def get_next_available_row(board, col, rows):
    """Get the next available row in the given column, or -1 if column is full."""
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def is_valid_input(user_input, cols):
    """Validate the user input for column selection."""
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col = ord(user_input.upper()) - ord('A')
    if col < 0 or col >= cols:
        return False
    return True

def get_column_from_input(user_input):
    """Convert user input letter to column index."""
    return ord(user_input.upper()) - ord('A')

def place_checker(board, row, col, checker):
    """Place a checker on the board at the given position."""
    board[row][col] = checker

def check_win(board, row, col, checker, rows, cols):
    """Check if the last placed checker results in a win."""
    # Directions: horizontal, vertical, diagonal (two directions)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
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

def get_player_move(board, current_player, checker, cols, rows):
    """Get a valid move from the current player."""
    while True:
        print(f"Player {checker}, please enter a column: ", end="")
        user_input = input().strip()
        
        if not is_valid_input(user_input, cols):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(
                chr(ord('A') + cols - 1)))
            continue
        
        col = get_column_from_input(user_input)
        next_row = get_next_available_row(board, col, rows)
        
        if next_row == -1:
            print("Column is full. Please choose another column.")
            continue
        
        return col, next_row

def play_game(rows, cols, num_players):
    """Main game loop."""
    board = initialize_board(rows, cols)
    
    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)
    
    print_board(board, cols)
    
    game_over = False
    winner = None
    
    while not game_over:
        checker = CHECKERS[current_player]
        col, row = get_player_move(board, current_player, checker, cols, rows)
        
        place_checker(board, row, col, checker)
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row, col, checker, rows, cols):
            print(f"Player {checker} won!")
            game_over = True
            winner = checker
        # Check for draw
        elif is_board_full(board, rows, cols):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % num_players

def main():
    """Entry point of the program."""
    num_players = 2
    play_game(ROWS, COLUMNS, num_players)

if __name__ == "__main__":
    main()
