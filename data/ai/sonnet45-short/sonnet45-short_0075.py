import random
import os

# Game Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.
COLUMN_LABELS = 'ABCDEFG'
EMPTY = '.'

def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "---" * COLS)
    print()

def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, enter column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ").upper()
        
        if len(choice) != 1 or choice not in COLUMN_LABELS[:COLS]:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[COLS-1]}.")
            continue
        
        return COLUMN_LABELS.index(choice)

def drop_piece(board, col, player):
    """
    Drop a piece in the specified column.
    Returns the row where the piece landed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    
    def check_direction(delta_row, delta_col):
        """Check for 4 in a row in a specific direction."""
        count = 1  # Count the piece we just placed
        
        # Check in positive direction
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += delta_row
            c += delta_col
        
        # Check in negative direction
        r, c = row - delta_row, col - delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= delta_row
            c -= delta_col
        
        return count >= 4
    
    # Check all four directions: horizontal, vertical, and two diagonals
    return (check_direction(0, 1) or   # Horizontal
            check_direction(1, 0) or   # Vertical
            check_direction(1, 1) or   # Diagonal \
            check_direction(1, -1))    # Diagonal /

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != EMPTY for col in range(COLS))

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"Player {PLAYERS[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        # Get valid column choice
        while True:
            col = get_column_input(current_player)
            row = drop_piece(board, col, current_player)
            
            if row != -1:
                break
            print("Column is full! Choose another column.")
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

def main():
    """Start the game and handle replay."""
    while True:
        play_game()
        
        replay = input("\nPlay again? (y/n): ").lower()
        if replay != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
