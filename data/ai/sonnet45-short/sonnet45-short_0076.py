import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for 4 players, etc.
COLUMN_LABELS = 'ABCDEFG'

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print(' +' + '---+' * COLS)
    
    for row in board:
        print(' | ' + ' | '.join(row) + ' |')
        print(' +' + '---+' * COLS)
    print()

def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return board[0][col] == ' '

def get_next_row(board, col):
    """Find the next available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def drop_piece(board, col, player):
    """Drop a piece into the specified column."""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = player
        return True
    return False

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        try:
            move = input(f"Player {player}, enter column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ").upper()
            
            if len(move) != 1 or move not in COLUMN_LABELS[:COLS]:
                print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[COLS-1]}.")
                continue
            
            col = COLUMN_LABELS.index(move)
            
            if not is_valid_move(board, col):
                print("That column is full! Choose another column.")
                continue
            
            return col
        
        except KeyboardInterrupt:
            print("\nGame interrupted!")
            exit()

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_idx = random.randint(0, len(PLAYERS) - 1)
    
    print_board(board)
    print(f"Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"Player {PLAYERS[current_player_idx]} goes first!\n")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_idx]
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
        
        # Move to next player
        current_player_idx = (current_player_idx + 1) % len(PLAYERS)

def main():
    """Entry point of the program."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
