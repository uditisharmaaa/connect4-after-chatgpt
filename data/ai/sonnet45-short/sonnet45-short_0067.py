import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
EMPTY = '.'
CONNECT_NUM = 4


def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  A B C D E F G")
    print(" +" + "-" * (NUM_COLS * 2 - 1) + "+")
    
    for row in board:
        print(" |" + " ".join(row) + "|")
    
    print(" +" + "-" * (NUM_COLS * 2 - 1) + "+")
    print("  A B C D E F G\n")


def get_column_input():
    """Get and validate column input from player."""
    while True:
        choice = input("Enter column (A-G): ").strip().upper()
        
        if len(choice) != 1:
            print("Please enter a single letter.")
            continue
            
        if choice < 'A' or choice > 'G':
            print("Invalid column. Choose A-G.")
            continue
            
        return ord(choice) - ord('A')  # Convert letter to column index


def drop_piece(board, col, symbol):
    """
    Drop a piece in the specified column.
    Returns the row where piece landed, or -1 if column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) created a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dx, dy in directions:
        count = 1  # Count the piece we just placed
        
        # Check in positive direction
        count += count_direction(board, row, col, dx, dy, symbol)
        
        # Check in negative direction
        count += count_direction(board, row, col, -dx, -dy, symbol)
        
        if count >= CONNECT_NUM:
            return True
    
    return False


def count_direction(board, row, col, dx, dy, symbol):
    """Count consecutive pieces in a given direction."""
    count = 0
    r, c = row + dx, col + dy
    
    while (0 <= r < NUM_ROWS and 
           0 <= c < NUM_COLS and 
           board[r][c] == symbol):
        count += 1
        r += dx
        c += dy
    
    return count


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != EMPTY for col in range(NUM_COLS))


def play_game():
    """Main game loop."""
    # Setup
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\n{'='*40}")
    print("       CONNECT 4 GAME")
    print(f"{'='*40}")
    print(f"\nPlayers: {', '.join(players)}")
    print(f"First player: {players[current_player_idx]}")
    input("\nPress Enter to start...")
    
    # Game loop
    while True:
        current_symbol = players[current_player_idx]
        print_board(board)
        print(f"Player {current_symbol}'s turn")
        
        # Get valid column
        while True:
            col = get_column_input()
            row = drop_piece(board, col, current_symbol)
            
            if row != -1:
                break
            else:
                print("That column is full. Try another.")
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f"{'='*40}")
            print(f"  Player {current_symbol} wins!")
            print(f"{'='*40}\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print(f"{'='*40}")
            print("  It's a draw!")
            print(f"{'='*40}\n")
            break
        
        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main():
    """Entry point for the game."""
    while True:
        play_game()
        
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
