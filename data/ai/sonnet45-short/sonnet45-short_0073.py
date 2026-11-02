import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Create empty board
def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(' ')
        board.append(row)
    return board

# Print the board
def print_board(board):
    print("\n  A B C D E F G")
    for i in range(ROWS):
        print(i + 1, end=" ")
        for j in range(COLS):
            print(board[i][j], end=" ")
        print()
    print()

# Check if column is valid and not full
def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != ' ':
        return False
    return True

# Drop piece in column
def drop_piece(board, col, symbol):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = symbol
            return i

# Check if there's a winner
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

# Check if board is full (draw)
def is_board_full(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

# Main game
def play_game():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(PLAYER_SYMBOLS[i])
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print("Players:", ", ".join(players))
    print("First player:", players[current_player_index])
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        os.system('clear')
        print_board(board)
        
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}'s turn")
        
        # Get valid input
        valid_input = False
        while not valid_input:
            move = input("Enter column (A-G): ").upper()
            
            if len(move) != 1 or move < 'A' or move > 'G':
                print("Invalid input! Enter a letter A-G")
                continue
            
            col = ord(move) - ord('A')
            
            if not is_valid_move(board, col):
                print("Column is full or invalid! Try again")
                continue
            
            valid_input = True
        
        # Make move
        drop_piece(board, col, current_symbol)
        
        # Check win
        if check_win(board, current_symbol):
            os.system('clear')
            print_board(board)
            print(f"Player {current_symbol} wins!")
            game_over = True
        # Check draw
        elif is_board_full(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
play_game()
