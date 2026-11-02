import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board():
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

# Display the board
def print_board(board):
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +" + "-" * 13 + "+")
    for row in range(ROWS):
        print(str(row + 1) + "|", end="")
        for col in range(COLS):
            print(board[row][col] + " ", end="")
        print("|")
    print(" +" + "-" * 13 + "+")
    print("  A B C D E F G\n")

# Drop a piece in a column
def drop_piece(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

# Check if a column is full
def is_column_full(board, col):
    return board[0][col] != ' '

# Validate player input
def get_valid_move(board, player_symbol):
    while True:
        move = input(f"Player {player_symbol}, enter column (A-G): ").upper()
        
        if len(move) != 1:
            print("Invalid input! Enter a single letter.")
            continue
        
        if move < 'A' or move > 'G':
            print("Invalid column! Choose A through G.")
            continue
        
        col = ord(move) - ord('A')
        
        if is_column_full(board, col):
            print("Column is full! Choose another column.")
            continue
        
        return col

# Check for a win
def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == symbol and
                board[row + 1][col - 1] == symbol and
                board[row + 2][col - 2] == symbol and
                board[row + 3][col - 3] == symbol):
                return True
    
    return False

# Check if the board is full (draw)
def is_board_full(board):
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

# Main game function
def play_game():
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
        
        col = get_valid_move(board, current_symbol)
        drop_piece(board, col, current_symbol)
        
        if check_win(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            game_over = True
        elif is_board_full(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
