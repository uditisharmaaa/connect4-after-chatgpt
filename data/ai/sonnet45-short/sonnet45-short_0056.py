import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Initialize the game board
def create_board():
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Display the board
def print_board(board):
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +" + "-" * (NUM_COLS * 2 - 1) + "+")
    for row in board:
        print(" |" + "|".join(row) + "|")
    print(" +" + "-" * (NUM_COLS * 2 - 1) + "+")
    print()

# Convert column letter to index
def column_to_index(col_letter):
    col_letter = col_letter.upper()
    if col_letter in 'ABCDEFG':
        return ord(col_letter) - ord('A')
    return -1

# Check if a column is valid and not full
def is_valid_move(board, col_index):
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    return board[0][col_index] == ' '

# Drop a piece in the specified column
def drop_piece(board, col_index, symbol):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = symbol
            return row
    return -1

# Check for a win
def check_win(board, row, col, symbol):
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == symbol:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == symbol:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < NUM_ROWS and c < NUM_COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(NUM_ROWS - 1 - row, col)
    start_col = col - min(NUM_ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < NUM_COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

# Check if the board is full (draw)
def is_board_full(board):
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

# Main game function
def play_game():
    board = create_board()
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"First player: {players[current_player_index]}")
    input("Press Enter to start...")
    
    while True:
        print_board(board)
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}'s turn")
        
        # Get valid input
        while True:
            col_input = input("Choose a column (A-G): ").strip()
            if not col_input:
                print("Please enter a column letter.")
                continue
            
            col_index = column_to_index(col_input)
            
            if col_index == -1:
                print("Invalid column. Please choose A-G.")
                continue
            
            if not is_valid_move(board, col_index):
                print("Column is full or invalid. Try again.")
                continue
            
            break
        
        # Drop the piece
        row = drop_piece(board, col_index, current_symbol)
        
        # Check for win
        if check_win(board, row, col_index, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
