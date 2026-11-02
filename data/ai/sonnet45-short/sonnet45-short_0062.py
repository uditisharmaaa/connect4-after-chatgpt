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
    """Display the board"""
    print("\n  A B C D E F G")
    print(" +" + "-" * 15 + "+")
    for row in range(ROWS):
        print(str(row) + "|", end="")
        for col in range(COLS):
            print(board[row][col] + " ", end="")
        print("|")
    print(" +" + "-" * 15 + "+")
    print("  A B C D E F G\n")

def is_valid_column(col_letter):
    """Check if the column letter is valid"""
    return col_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def column_letter_to_number(col_letter):
    """Convert column letter to number (A=0, B=1, etc.)"""
    return ord(col_letter) - ord('A')

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col] != ' '

def drop_piece(board, col, piece):
    """Drop a piece in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return row
    return -1

def check_win(board, row, col, piece):
    """Check if the last move resulted in a win"""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == piece:
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
        if board[r][c] == piece:
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
        if board[r][c] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
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
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    os.system('clear')
    print("=== CONNECT 4 ===")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        os.system('clear')
        print_board(board)
        
        current_piece = players[current_player_index]
        print(f"Player {current_piece}'s turn")
        
        # Get valid input
        valid_move = False
        while not valid_move:
            col_input = input("Choose column (A-G): ").upper()
            
            if not is_valid_column(col_input):
                print("Invalid column! Please choose A-G.")
                continue
            
            col = column_letter_to_number(col_input)
            
            if is_column_full(board, col):
                print("That column is full! Choose another.")
                continue
            
            valid_move = True
        
        # Drop the piece
        row = drop_piece(board, col, current_piece)
        
        # Check for win
        if check_win(board, row, col, current_piece):
            os.system('clear')
            print_board(board)
            print(f"*** Player {current_piece} WINS! ***")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            os.system('clear')
            print_board(board)
            print("*** DRAW! The board is full! ***")
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    print("\nThanks for playing!")

# Start the game
play_game()
