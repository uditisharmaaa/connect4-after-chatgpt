import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board"""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print('\n  A   B   C   D   E   F   G')
    print('-----------------------------')
    for row in range(ROWS):
        print('|', end='')
        for col in range(COLS):
            print(' ' + board[row][col] + ' |', end='')
        print()
        print('-----------------------------')
    print()

def is_valid_move(board, col):
    """Check if a column has space for a piece"""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def drop_piece(board, col, symbol):
    """Drop a piece in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move created a winning connection"""
    
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
    
    # Check diagonal (bottom-left to top-right)
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
    
    # Check diagonal (top-left to bottom-right)
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

def get_column_input():
    """Get and validate column input from user"""
    while True:
        user_input = input('Enter column (A-G): ').upper()
        if len(user_input) == 1 and user_input in COLUMN_LABELS:
            return COLUMN_LABELS.index(user_input)
        else:
            print('Invalid input! Please enter a letter from A to G.')

def play_game():
    """Main game function"""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print('Welcome to Connect 4!')
    print(f'Players: {", ".join(players)}')
    print(f'Starting player: {players[current_player_index]}')
    input('Press Enter to start...')
    
    game_over = False
    
    while not game_over:
        print_board(board)
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}'s turn")
        
        # Get valid move
        valid_move = False
        while not valid_move:
            col = get_column_input()
            if is_valid_move(board, col):
                valid_move = True
            else:
                print('That column is full! Choose another column.')
        
        # Drop piece and check for win
        row = drop_piece(board, col, current_symbol)
        
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f'Player {current_symbol} wins!')
            game_over = True
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    print('Game Over!')

# Start the game
play_game()
