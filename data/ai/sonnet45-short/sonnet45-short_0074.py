import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for 4 players, etc.
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """
    Creates an empty game board represented as a 2D list.
    Each cell contains a space character initially.
    """
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """
    Displays the current game board to the console.
    Shows column labels at the top and the grid with pieces.
    """
    # Clear the screen for a clean display
    os.system('clear')
    
    # Print column labels
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print(' ' + '---' * COLS + '--')
    
    # Print each row with row numbers
    for i, row in enumerate(board):
        print(str(i + 1) + '| ' + ' | '.join(row) + ' |')
        print(' ' + '---' * COLS + '--')
    print()

def is_valid_move(board, col):
    """
    Checks if a move is valid (column exists and has space).
    Returns True if the top row of the column is empty.
    """
    return 0 <= col < COLS and board[0][col] == ' '

def drop_piece(board, col, piece):
    """
    Drops a piece into the specified column.
    The piece falls to the lowest available row in that column.
    Returns the row where the piece landed.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row
    return -1  # Column is full (shouldn't happen if is_valid_move is used)

def check_win(board, row, col, piece):
    """
    Checks if the last move at (row, col) resulted in a win.
    Checks all four directions: horizontal, vertical, and both diagonals.
    Returns True if four in a row are found.
    """
    # Helper function to count consecutive pieces in a direction
    def count_direction(delta_row, delta_col):
        count = 0
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
            count += 1
            r += delta_row
            c += delta_col
        return count
    
    # Check horizontal (left + right + 1 for current piece)
    horizontal = count_direction(0, -1) + count_direction(0, 1) + 1
    
    # Check vertical (only need to check downward)
    vertical = count_direction(1, 0) + 1
    
    # Check diagonal (bottom-left to top-right)
    diagonal1 = count_direction(1, -1) + count_direction(-1, 1) + 1
    
    # Check diagonal (top-left to bottom-right)
    diagonal2 = count_direction(-1, -1) + count_direction(1, 1) + 1
    
    # Win if any direction has 4 or more consecutive pieces
    return horizontal >= 4 or vertical >= 4 or diagonal1 >= 4 or diagonal2 >= 4

def is_board_full(board):
    """
    Checks if the board is completely full (a draw condition).
    Returns True if no empty spaces remain in the top row.
    """
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, current_player):
    """
    Prompts the current player for their move and validates the input.
    Continues to prompt until a valid move is entered.
    Returns the column index (0-6).
    """
    while True:
        move = input(f"Player {current_player}, enter column (A-G): ").strip().upper()
        
        # Validate input is a single character
        if len(move) != 1:
            print("Invalid input! Please enter a single letter A-G.")
            continue
        
        # Check if input is a valid column label
        if move not in COLUMN_LABELS:
            print("Invalid column! Please enter a letter from A to G.")
            continue
        
        # Convert letter to column index
        col = COLUMN_LABELS.index(move)
        
        # Check if the column has space
        if not is_valid_move(board, col):
            print("Column is full! Choose another column.")
            continue
        
        return col

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the game board
    board = create_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print(f"Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"Player {PLAYERS[current_player_index]} goes first!\n")
    input("Press Enter to start...")
    
    # Game loop
    while True:
        current_player = PLAYERS[current_player_index]
        
        # Display the current board
        print_board(board)
        
        # Get the player's move
        col = get_player_move(board, current_player)
        
        # Drop the piece and get the row where it landed
        row = drop_piece(board, col, current_player)
        
        # Check if this move wins the game
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        # Check if the board is full (draw)
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Run the game
if __name__ == "__main__":
    play_game()
