import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board."""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the board."""
    print("\n  A   B   C   D   E   F   G")
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
        if row < ROWS - 1:
            print("|---|---|---|---|---|---|---|")
    print("=============================")

def get_column():
    """Get column input from player."""
    while True:
        col_input = input("Enter column (A-G): ").upper()
        if len(col_input) == 1 and col_input >= 'A' and col_input <= 'G':
            return ord(col_input) - ord('A')
        else:
            print("Invalid input! Please enter a letter from A to G.")

def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return board[0][col] == ' '

def drop_piece(board, col, player):
    """Drop a piece in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the current move wins the game."""
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
    start_row = row - min(row, col)
    start_col = col - min(row, col)
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
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
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
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    os.system('clear')
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    print("\nConnect 4 pieces in a row to win!")
    input("\nPress Enter to start...")
    
    while True:
        os.system('clear')
        print_board(board)
        
        current_player = players[current_player_index]
        print(f"\nPlayer {current_player}'s turn")
        
        # Get valid move
        while True:
            col = get_column()
            if is_valid_move(board, col):
                break
            else:
                print("Column is full! Choose another column.")
        
        # Drop piece and check for win
        row = drop_piece(board, col, current_player)
        
        os.system('clear')
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"\n*** Player {current_player} wins! ***")
            break
        
        if is_board_full(board):
            print("\n*** It's a draw! ***")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    print("\nThanks for playing!")

# Start the game
play_game()
