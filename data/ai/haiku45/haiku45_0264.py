import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Create and return a 2D board with all cells initialized to spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board, rows, cols):
    """Print the Connect 4 board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()

def is_valid_column(column_letter, cols):
    """Check if the column letter is valid."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    col_index = ord(column_letter.upper()) - ord('A')
    return 0 <= col_index < cols

def column_letter_to_index(column_letter):
    """Convert column letter to index."""
    return ord(column_letter.upper()) - ord('A')

def is_column_full(board, col_index, rows):
    """Check if a column is completely filled."""
    return board[0][col_index] != ' '

def place_checker(board, col_index, checker, rows):
    """Place a checker in the specified column and return the row it was placed in."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return -1

def check_win(board, row, col, checker, rows, cols):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board, rows, cols):
    """Check if the board is completely filled."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == ' ':
                return False
    return True

def get_player_move(player_checker, cols):
    """Get and validate the player's move."""
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_column(move, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = column_letter_to_index(move)
        
        if is_column_full(board, col_index, ROWS):
            print("This column is full. Please choose another column.")
            continue
        
        return col_index

def main():
    """Main game loop."""
    global board
    
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Initialize players
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, ROWS, COLS)
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player move
        col_index = get_player_move(current_player, COLS)
        
        # Place checker
        row = place_checker(board, col_index, current_player, ROWS)
        
        # Print board
        print_board(board, ROWS, COLS)
        
        # Check for win
        if check_win(board, row, col_index, current_player, ROWS, COLS):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
