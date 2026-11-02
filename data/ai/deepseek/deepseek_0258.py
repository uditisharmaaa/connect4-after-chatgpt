import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only take necessary players

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def is_valid_column(col_input):
    """Check if the user's column input is valid (uppercase letter within range)."""
    if len(col_input) != 1:
        return False
    col_char = col_input.upper()
    return 'A' <= col_char <= chr(65 + COLS - 1)

def get_column_index(col_input):
    """Convert column letter (e.g., 'A') to column index (0-based)."""
    return ord(col_input.upper()) - ord('A')

def drop_checker(board, col, player):
    """Drop a player's checker into the specified column.
    Returns the row where the checker was placed, or -1 if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Column is full

def check_win(board, row, col, player):
    """Check if the player has won by placing a checker at (row, col) in the board."""
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))  # Random first player
    
    clear_screen()
    print_board(board)
    
    while True:
        player_char = PLAYERS[current_player]
        col_input = input(f"Player {player_char}, please enter a column: ").strip()
        
        # Validate input
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C, ...).")
            continue
        
        col = get_column_index(col_input)
        row = drop_checker(board, col, player_char)
        
        if row == -1:
            print("That column is full. Please choose another column.")
            continue
        
        # Check for win or draw
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col, player_char):
            print(f"Player {player_char} won!")
            break
        elif is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch players
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
