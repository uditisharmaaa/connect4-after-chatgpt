import random
import os

# Constants for game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for 4 players, etc.
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """
    Create an empty game board represented as a 2D list.
    Each cell contains a space character initially.
    """
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """
    Display the game board with column labels and row numbers.
    """
    print("\n  " + " ".join(COLUMN_LABELS))
    print(" +" + "-" * (COLS * 2 - 1) + "+")
    
    # Print each row with its row number
    for i, row in enumerate(board):
        print(f"{i}|" + "|".join(row) + "|")
    
    print(" +" + "-" * (COLS * 2 - 1) + "+")
    print("  " + " ".join(COLUMN_LABELS) + "\n")

def get_valid_move(board, player):
    """
    Prompt the current player for a column choice and validate the input.
    Returns the column index (0-6) for a valid move.
    """
    while True:
        move = input(f"Player {player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").strip().upper()
        
        # Check if input is a valid column label
        if move not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        
        # Convert column label to index
        col = COLUMN_LABELS.index(move)
        
        # Check if column is not full
        if board[0][col] != ' ':
            print("That column is full! Choose another column.")
            continue
        
        return col

def drop_piece(board, col, player):
    """
    Drop a player's piece into the specified column.
    The piece falls to the lowest available row in that column.
    """
    # Start from the bottom row and find the first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row

def check_winner(board, row, col, player):
    """
    Check if the last move at (row, col) created a winning connection.
    Returns True if the player won, False otherwise.
    Checks horizontal, vertical, and both diagonal directions.
    """
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find the starting position of this diagonal
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    # Find the starting position of this diagonal
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def check_draw(board):
    """
    Check if the board is full (draw condition).
    Returns True if no empty spaces remain in the top row.
    """
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the game board
    board = create_board()
    
    # Randomly select which player goes first
    current_player_idx = random.randint(0, len(PLAYERS) - 1)
    
    # Clear screen and display initial board
    os.system('clear')
    print("=" * 30)
    print("   CONNECT 4 GAME")
    print("=" * 30)
    print(f"\nPlayers: {', '.join(PLAYERS)}")
    print(f"First player: {PLAYERS[current_player_idx]}")
    
    # Main game loop
    while True:
        current_player = PLAYERS[current_player_idx]
        
        # Display the current board
        print_board(board)
        
        # Get valid move from current player
        col = get_valid_move(board, current_player)
        
        # Drop the piece and get the row where it landed
        row = drop_piece(board, col, current_player)
        
        # Clear screen for next display
        os.system('clear')
        
        # Check if current player won
        if check_winner(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} WINS! 🎉")
            break
        
        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("It's a DRAW! The board is full.")
            break
        
        # Switch to next player
        current_player_idx = (current_player_idx + 1) % len(PLAYERS)

def main():
    """
    Entry point of the program. Allows for multiple games.
    """
    while True:
        play_game()
        
        # Ask if players want to play again
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break
        os.system('clear')

# Run the game
if __name__ == "__main__":
    main()
