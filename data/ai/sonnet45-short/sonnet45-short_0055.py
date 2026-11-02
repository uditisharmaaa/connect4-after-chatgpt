# Connect 4 Game
# Intro CS Class Project

import random
import os

# CONSTANTS
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print("\n  CONNECT 4")
    print("=" * 29)
    
    # Print column labels
    print("  ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print("\n  " + "---" * COLS)
    
    # Print board rows
    for row in board:
        print("  |", end="")
        for cell in row:
            print(f"{cell}|", end="")
        print()
    
    # Print bottom border
    print("  " + "---" * COLS)
    print()

def get_num_players():
    """Get and validate the number of players."""
    while True:
        try:
            num = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num <= MAX_PLAYERS:
                return num
            else:
                print(f"Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        move = input(f"Player {player}, enter column (A-G): ").upper().strip()
        
        if len(move) != 1:
            print("Please enter a single column letter.")
            continue
        
        if move not in COLUMN_LABELS:
            print(f"Invalid column. Please enter a letter from A to G.")
            continue
        
        return COLUMN_LABELS.index(move)

def drop_piece(board, col, player):
    """
    Drop a piece in the specified column.
    Returns the row where the piece landed, or -1 if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """
    Check if the most recent move resulted in a win.
    Checks horizontal, vertical, and both diagonal directions.
    """
    
    def check_direction(dr, dc):
        """Check a specific direction for 4 in a row."""
        count = 1  # Count the placed piece itself
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        return count >= 4
    
    # Check horizontal
    if check_direction(0, 1):
        return True
    
    # Check vertical
    if check_direction(1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(1, -1):
        return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    print("=" * 29)
    print("  WELCOME TO CONNECT 4!")
    print("=" * 29)
    print("\nConnect 4 pieces in a row to win!")
    print("(horizontally, vertically, or diagonally)\n")
    
    # Setup
    num_players = get_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    board = create_board()
    
    # Randomly select first player
    current_player_index = random.randint(0, num_players - 1)
    current_player = players[current_player_index]
    
    print(f"\nRandomly selected: Player {current_player} goes first!")
    input("Press Enter to start the game...")
    
    # Game loop
    moves_made = 0
    max_moves = ROWS * COLS
    
    while moves_made < max_moves:
        print_board(board)
        
        # Show current player
        print(f"Current Player: {current_player}")
        
        # Get valid move
        while True:
            col = get_column_input(current_player)
            row = drop_piece(board, col, current_player)
            
            if row != -1:
                break
            else:
                print("That column is full! Choose another column.")
        
        moves_made += 1
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print("=" * 29)
            print(f"  PLAYER {current_player} WINS!")
            print("=" * 29)
            return
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("=" * 29)
            print("  GAME ENDS IN A DRAW!")
            print("=" * 29)
            return
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players
        current_player = players[current_player_index]

def main():
    """Main program entry point."""
    while True:
        play_game()
        
        # Ask to play again
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y' and play_again != 'yes':
            print("\nThanks for playing Connect 4!")
            break

if __name__ == "__main__":
    main()
