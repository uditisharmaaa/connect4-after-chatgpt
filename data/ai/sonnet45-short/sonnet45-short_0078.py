import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board"""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  A   B   C   D   E   F   G")
    print(" " + "---" * COLS + "--")
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        print(" " + "---" * COLS + "--")
    print()

def get_column():
    """Get and validate column input from player"""
    while True:
        choice = input("Choose a column (A-G): ").upper()
        if len(choice) == 1 and choice >= 'A' and choice <= 'G':
            return ord(choice) - ord('A')  # Convert A-G to 0-6
        print("Invalid input! Please enter a letter from A to G.")

def drop_piece(board, col, player):
    """Drop a piece in the specified column"""
    # Start from bottom row and go up
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Column is full

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col] != ' '

def check_win(board, row, col, player):
    """Check if the last move resulted in a win"""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    # Count along diagonal
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find starting position
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    # Count along diagonal
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full"""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop"""
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    
    # Pick random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    while True:
        current_player = players[current_player_index]
        print_board(board)
        
        print(f"Player {current_player}'s turn")
        
        # Get valid column choice
        while True:
            col = get_column()
            if not is_column_full(board, col):
                break
            print("That column is full! Choose another column.")
        
        # Drop the piece
        row = drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
