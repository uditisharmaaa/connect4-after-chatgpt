import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board"""
    board = []
    for row in range(ROWS):
        new_row = []
        for col in range(COLS):
            new_row.append(' ')
        board.append(new_row)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +-+-+-+-+-+-+-+")
    for row in range(ROWS):
        print(str(row + 1) + "|", end="")
        for col in range(COLS):
            print(board[row][col] + "|", end="")
        print()
    print(" +-+-+-+-+-+-+-+")
    print()

def get_player_move(player):
    """Get and validate player input"""
    while True:
        move = input("Player " + player + ", enter column (A-G): ").upper()
        
        if len(move) != 1:
            print("Please enter a single letter!")
            continue
            
        if move not in COLUMN_LABELS:
            print("Invalid column! Choose A-G.")
            continue
            
        return move

def get_column_number(column_letter):
    """Convert column letter to number"""
    for i in range(len(COLUMN_LABELS)):
        if COLUMN_LABELS[i] == column_letter:
            return i
    return -1

def is_column_full(board, col):
    """Check if a column is full"""
    return board[0][col] != ' '

def drop_piece(board, col, player):
    """Drop a piece in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win"""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count = count + 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
            count = count + 1
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
        if board[r][c] == player:
            count = count + 1
            if count == 4:
                return True
        else:
            count = 0
        r = r + 1
        c = c + 1
    
    # Check diagonal (up-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count = count + 1
            if count == 4:
                return True
        else:
            count = 0
        r = r - 1
        c = c + 1
    
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
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print("Welcome to Connect 4!")
    print("Players:", ', '.join(PLAYERS))
    print()
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get valid move
        while True:
            column_letter = get_player_move(current_player)
            column_number = get_column_number(column_letter)
            
            if is_column_full(board, column_number):
                print("That column is full! Choose another.")
            else:
                break
        
        # Drop piece and check for win
        row = drop_piece(board, column_number, current_player)
        
        if check_win(board, row, column_number, current_player):
            print_board(board)
            print("Player " + current_player + " wins!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Start the game
play_game()
