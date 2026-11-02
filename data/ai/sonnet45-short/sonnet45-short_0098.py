import random
import os

# Constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Available player symbols
NUM_PLAYERS = 2  # Change this to 2-5 to set number of players

# Column labels for user input
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def create_board():
    """
    Create an empty game board.
    Returns a 2D list filled with spaces representing empty cells.
    """
    board = []
    for row in range(NUM_ROWS):
        board.append([' '] * NUM_COLS)
    return board


def print_board(board):
    """
    Display the current state of the board.
    Shows column labels at top and the grid with row separators.
    """
    # Print column labels
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print('  ' + '---' * NUM_COLS + '--')
    
    # Print each row of the board
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('  ' + '---' * NUM_COLS + '--')
    print()


def get_valid_column(board):
    """
    Get and validate column input from the player.
    Returns the column index (0-6) if valid, or None if invalid.
    """
    user_input = input("Enter column (A-G): ").strip().upper()
    
    # Check if input is a single character and a valid column label
    if len(user_input) != 1 or user_input not in COLUMN_LABELS:
        print("Invalid column! Please enter A-G.")
        return None
    
    col_index = COLUMN_LABELS.index(user_input)
    
    # Check if column is full (top row occupied)
    if board[0][col_index] != ' ':
        print("Column is full! Choose another column.")
        return None
    
    return col_index


def drop_piece(board, col, player):
    """
    Drop a player's piece into the specified column.
    The piece falls to the lowest available row in that column.
    """
    # Start from bottom row and work upward
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row  # Return the row where piece landed
    return -1  # Should never reach here if input validation works


def check_win(board, row, col, player):
    """
    Check if the current move resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    Returns True if player has 4 in a row, False otherwise.
    """
    
    def count_direction(delta_row, delta_col):
        """
        Count consecutive pieces in a given direction.
        delta_row and delta_col define the direction to check.
        """
        count = 0
        r, c = row, col
        
        # Count in the positive direction
        while (0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and 
               board[r][c] == player):
            count += 1
            r += delta_row
            c += delta_col
        
        return count - 1  # Subtract 1 to not count the original position twice
    
    # Check horizontal (left + right)
    horizontal = 1 + count_direction(0, 1) + count_direction(0, -1)
    
    # Check vertical (down + up, though up won't matter in Connect 4)
    vertical = 1 + count_direction(1, 0) + count_direction(-1, 0)
    
    # Check diagonal (bottom-right to top-left)
    diagonal1 = 1 + count_direction(1, 1) + count_direction(-1, -1)
    
    # Check diagonal (bottom-left to top-right)
    diagonal2 = 1 + count_direction(1, -1) + count_direction(-1, 1)
    
    # Win if any direction has 4 or more in a row
    return horizontal >= 4 or vertical >= 4 or diagonal1 >= 4 or diagonal2 >= 4


def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if top row is completely filled, False otherwise.
    """
    # If top row has no empty spaces, board is full
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True


def play_game():
    """
    Main game loop that controls the flow of the game.
    """
    # Initialize the game
    board = create_board()
    active_players = PLAYERS[:NUM_PLAYERS]  # Select the first N players
    current_player_index = random.randint(0, NUM_PLAYERS - 1)  # Random first player
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(active_players)}")
    print(f"Player {active_players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    # Main game loop
    while True:
        os.system('clear')  # Clear the screen
        print_board(board)
        
        current_player = active_players[current_player_index]
        print(f"Player {current_player}'s turn")
        
        # Get valid column input
        col = get_valid_column(board)
        if col is None:
            input("Press Enter to continue...")
            continue
        
        # Drop the piece and get the row where it landed
        row = drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        # Check for draw
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
