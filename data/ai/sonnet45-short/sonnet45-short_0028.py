import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2-5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board."""
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

def get_valid_column(board, player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[COLS-1]}): ").upper().strip()
        
        # Check if input is valid column label
        if choice not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[COLS-1]}.")
            continue
        
        col = COLUMN_LABELS.index(choice)
        
        # Check if column is full
        if board[0][col] != ' ':
            print("That column is full! Choose another one.")
            continue
        
        return col

def drop_piece(board, col, player):
    """Drop a piece in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the current move results in a win."""
    
    # Check horizontal
    def check_direction(dr, dc):
        count = 1
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
    
    # Check all four directions: horizontal, vertical, diagonal /, diagonal \
    return (check_direction(0, 1) or  # Horizontal
            check_direction(1, 0) or  # Vertical
            check_direction(1, 1) or  # Diagonal \
            check_direction(1, -1))   # Diagonal /

def check_draw(board):
    """Check if the board is full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    # Validate NUM_PLAYERS
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5!")
        return
    
    # Set up players
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board()
    
    # Randomly choose first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Players: {', '.join(players)}")
    print(f"\nPlayer {players[current_player_idx]} goes first!")
    input("Press Enter to start...")
    
    # Game loop
    moves = 0
    max_moves = ROWS * COLS
    
    while moves < max_moves:
        print_board(board)
        current_player = players[current_player_idx]
        
        # Get valid move
        col = get_valid_column(board, current_player)
        
        # Drop piece and get row where it landed
        row = drop_piece(board, col, current_player)
        moves += 1
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            return
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            return
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

def main():
    """Main function to start the game."""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
