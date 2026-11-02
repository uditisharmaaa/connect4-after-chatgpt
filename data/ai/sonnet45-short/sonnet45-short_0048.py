import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMNS = 'ABCDEFG'

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  A B C D E F G')
    print(' +-+-+-+-+-+-+-+')
    for row in board:
        print(' |' + '|'.join(row) + '|')
        print(' +-+-+-+-+-+-+-+')
    print()

def drop_piece(board, col, piece):
    """Drop a piece in the specified column. Returns True if successful."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return True
    return False

def is_valid_column(col_letter):
    """Check if column input is valid."""
    return col_letter.upper() in COLUMNS

def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != ' '

def check_win(board, piece):
    """Check if the current piece has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == piece and
                board[row][col + 1] == piece and
                board[row][col + 2] == piece and
                board[row][col + 3] == piece):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == piece and
                board[row + 1][col] == piece and
                board[row + 2][col] == piece and
                board[row + 3][col] == piece):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == piece and
                board[row + 1][col + 1] == piece and
                board[row + 2][col + 2] == piece and
                board[row + 3][col + 3] == piece):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == piece and
                board[row + 1][col - 1] == piece and
                board[row + 2][col - 2] == piece and
                board[row + 3][col - 3] == piece):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        col_input = input(f"Player {player}, choose a column (A-G): ").strip()
        
        if not col_input:
            print("Please enter a column letter.")
            continue
        
        if not is_valid_column(col_input):
            print("Invalid column. Please choose A-G.")
            continue
        
        col_index = COLUMNS.index(col_input.upper())
        
        if is_column_full(board, col_index):
            print("That column is full. Choose another.")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Welcome to Connect 4!")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"\nPlayer {PLAYERS[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        col = get_player_move(board, current_player)
        drop_piece(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
