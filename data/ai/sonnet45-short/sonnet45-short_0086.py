import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board"""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the board"""
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +" + "-" * 14 + "+")
    for row in range(ROWS):
        print(str(row + 1) + "|", end="")
        for col in range(COLS):
            print(board[row][col] + " ", end="")
        print("|")
    print(" +" + "-" * 14 + "+")
    print("  A B C D E F G\n")

def is_valid_column(col_letter):
    """Check if column input is valid"""
    return col_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def column_to_index(col_letter):
    """Convert column letter to index"""
    return ord(col_letter) - ord('A')

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col] != ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move created a win"""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (down-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (up-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
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
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        print_board(board)
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}'s turn")
        
        # Get valid input
        valid_move = False
        while not valid_move:
            col_input = input("Enter column (A-G): ").upper()
            
            if len(col_input) != 1 or not is_valid_column(col_input):
                print("Invalid input! Please enter a letter A-G.")
                continue
            
            col = column_to_index(col_input)
            
            if is_column_full(board, col):
                print("That column is full! Choose another.")
                continue
            
            valid_move = True
        
        # Drop the piece
        row = drop_piece(board, col, current_symbol)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    print("\nThanks for playing!")

# Start the game
play_game()
