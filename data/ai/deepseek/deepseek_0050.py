import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Players' tokens in order
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the screen before printing the board
    
    # Print column headers (A, B, C, etc.)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows with borders
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    print('+---' * COLS + '+')

def get_valid_column(board):
    """Prompt the player for a column and validate the input."""
    while True:
        try:
            col = input("Player {}, please enter a column: ".format(current_player)).upper()
            if len(col) != 1 or not col.isalpha():
                print("Please enter a single letter (A-{}).".format(chr(65 + COLS - 1)))
                continue
            
            col_num = ord(col) - ord('A')
            if col_num < 0 or col_num >= COLS:
                print("Column must be between A and {}.".format(chr(65 + COLS - 1)))
                continue
            
            if board[0][col_num] != ' ':
                print("Column {} is full. Please choose another.".format(col))
                continue
            
            return col_num
        
        except (EOFError, KeyboardInterrupt):
            print("\nGame interrupted. Exiting.")
            exit()

def place_checker(board, col_num, player_token):
    """Place the player's token in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_num] == ' ':
            board[row][col_num] = player_token
            return row  # Return the row where the token was placed
    return -1  # Column is full (should not happen due to prior validation)

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    player_token = board[row][col]
    
    for dr, dc in directions:
        count = 1  # Include the current token
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely filled."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    global current_player
    
    # Initialize game
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    player_tokens = PLAYERS[:NUM_PLAYERS]
    
    print("Player {} starts first!".format(player_tokens[current_player]))
    
    # Main game loop
    while True:
        print_board(board)
        
        # Get valid column input
        col_num = get_valid_column(board)
        
        # Place the token and get the row
        row = place_checker(board, col_num, player_tokens[current_player])
        
        # Check for win
        if check_win(board, row, col_num):
            print_board(board)
            print("Player {} won!".format(player_tokens[current_player]))
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
