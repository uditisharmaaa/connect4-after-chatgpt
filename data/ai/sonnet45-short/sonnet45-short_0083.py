import random
import os

# Game Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.
EMPTY = '.'

def create_board():
    """Create an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  " + " ".join(COLUMN_LABELS))
    print("  " + "-" * (COLS * 2 - 1))
    
    for row in board:
        print("  " + " ".join(row))
    print()

def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return board[0][col] == EMPTY

def get_next_row(board, col):
    """Find the next available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
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
    """Check if the current player has won."""
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
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw)."""
    return all(board[0][col] != EMPTY for col in range(COLS))

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        try:
            move = input(f"Player {player}, enter column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").upper().strip()
            
            if move not in COLUMN_LABELS:
                print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue
            
            col = COLUMN_LABELS.index(move)
            
            if not is_valid_move(board, col):
                print("Column is full! Choose another column.")
                continue
            
            return col
        
        except (ValueError, IndexError):
            print("Invalid input! Please try again.")

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print(f"\n{'=' * 30}")
    print("  CONNECT 4")
    print(f"{'=' * 30}")
    print(f"\nPlayers: {', '.join(PLAYERS)}")
    print(f"Starting player: {PLAYERS[current_player_index]}\n")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        col = get_player_move(board, current_player)
        drop_piece(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉\n")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

def main():
    """Start the game and handle replay."""
    while True:
        play_game()
        
        replay = input("Play again? (y/n): ").lower().strip()
        if replay != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
