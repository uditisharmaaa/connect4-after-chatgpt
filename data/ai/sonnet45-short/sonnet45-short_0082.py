import random
import os

# Constants for game configuration
NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Available player symbols
NUM_PLAYERS = 2  # Change this to 2-5 to set number of players

def create_board():
    """
    Create and return an empty game board.
    Board is a 2D list with NUM_ROWS rows and NUM_COLS columns.
    """
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """
    Display the current game board with column labels (A-G).
    """
    os.system('clear')  # Clear the screen
    
    # Print column labels
    print('  A   B   C   D   E   F   G')
    
    # Print each row with separators
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('-' * 29)  # Separator line

def get_column_input():
    """
    Get and validate column input from the player.
    Returns the column index (0-6) or -1 if input is invalid.
    """
    user_input = input("Enter column (A-G): ").strip().upper()
    
    # Check if input is a single character and a valid column letter
    if len(user_input) == 1 and 'A' <= user_input <= 'G':
        # Convert letter to column index (A=0, B=1, etc.)
        return ord(user_input) - ord('A')
    
    return -1  # Invalid input

def is_valid_move(board, col):
    """
    Check if a move is valid (column exists and has space).
    Returns True if the top row of the column is empty.
    """
    return 0 <= col < NUM_COLS and board[0][col] == ' '

def drop_piece(board, col, player):
    """
    Drop a piece into the specified column for the current player.
    The piece falls to the lowest available row in that column.
    Returns the row where the piece landed.
    """
    # Start from the bottom row and work up
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Should never happen if is_valid_move was checked

def check_win(board, row, col, player):
    """
    Check if the last move at (row, col) created a winning condition.
    Checks horizontal, vertical, and both diagonal directions.
    Returns True if player won, False otherwise.
    """
    
    # Helper function to count consecutive pieces in a given direction
    def count_direction(row_dir, col_dir):
        count = 0
        r, c = row + row_dir, col + col_dir
        
        # Keep counting while in bounds and matching player symbol
        while (0 <= r < NUM_ROWS and 
               0 <= c < NUM_COLS and 
               board[r][c] == player):
            count += 1
            r += row_dir
            c += col_dir
        
        return count
    
    # Check all four directions (horizontal, vertical, two diagonals)
    # For each direction, count both ways and add 1 for the current piece
    
    # Horizontal: left + right + 1
    if count_direction(0, -1) + count_direction(0, 1) + 1 >= 4:
        return True
    
    # Vertical: down + up + 1 (only need to check down in practice)
    if count_direction(1, 0) + count_direction(-1, 0) + 1 >= 4:
        return True
    
    # Diagonal (down-right to up-left): / direction
    if count_direction(1, 1) + count_direction(-1, -1) + 1 >= 4:
        return True
    
    # Diagonal (down-left to up-right): \ direction
    if count_direction(1, -1) + count_direction(-1, 1) + 1 >= 4:
        return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if the top row has no empty spaces.
    """
    return all(board[0][col] != ' ' for col in range(NUM_COLS))

def play_game():
    """
    Main game loop that runs the Connect 4 game.
    """
    # Initialize game
    board = create_board()
    active_players = PLAYERS[:NUM_PLAYERS]  # Get the first NUM_PLAYERS symbols
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Welcome to Connect 4!")
    print(f"Players: {', '.join(active_players)}")
    print(f"Starting player: {active_players[current_player_index]}")
    input("Press Enter to start...")
    
    # Main game loop
    while True:
        current_player = active_players[current_player_index]
        
        # Display the board
        print_board(board)
        print(f"\nPlayer {current_player}'s turn")
        
        # Get valid move from player
        while True:
            col = get_column_input()
            
            # Validate the input
            if col == -1:
                print("Invalid input! Please enter a letter A-G.")
                continue
            
            if not is_valid_move(board, col):
                print("Invalid move! Column is full or doesn't exist. Try again.")
                continue
            
            break  # Valid move, exit input loop
        
        # Make the move
        row = drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"\n🎉 Player {current_player} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("\nIt's a draw! The board is full.")
            break
        
        # Move to next player (cycle through players)
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
