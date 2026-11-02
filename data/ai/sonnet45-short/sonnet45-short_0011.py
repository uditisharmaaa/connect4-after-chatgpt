import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for 4 players, etc.
CONNECT_LENGTH = 4


def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def display_board(board):
    """Display the game board."""
    os.system('clear')
    
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print(' ' + '---' * COLS + '--')
    
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print(' ' + '---' * COLS + '--')
    print()


def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").upper().strip()
        
        if choice in COLUMN_LABELS:
            return COLUMN_LABELS.index(choice)
        else:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")


def drop_piece(board, col, player):
    """Drop a piece in the specified column. Returns True if successful, False if column is full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False


def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - CONNECT_LENGTH + 1):
            if all(board[row][col + i] == player for i in range(CONNECT_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - CONNECT_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(CONNECT_LENGTH)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - CONNECT_LENGTH + 1):
        for col in range(COLS - CONNECT_LENGTH + 1):
            if all(board[row + i][col + i] == player for i in range(CONNECT_LENGTH)):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - CONNECT_LENGTH + 1):
        for col in range(CONNECT_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player for i in range(CONNECT_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))


def play_game():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    print(f"\nPlayers: {', '.join(PLAYERS)}")
    print(f"First player: {PLAYERS[current_player_index]}")
    input("\nPress Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        display_board(board)
        
        # Get valid column input
        while True:
            col = get_column_input(current_player)
            if drop_piece(board, col, current_player):
                break
            else:
                print("Column is full! Choose another column.")
        
        # Check for win
        if check_win(board, current_player):
            display_board(board)
            print("=" * 40)
            print(f"   Player {current_player} WINS!")
            print("=" * 40)
            break
        
        # Check for draw
        if check_draw(board):
            display_board(board)
            print("=" * 40)
            print("      It's a DRAW!")
            print("=" * 40)
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)


def main():
    """Main function to run the game."""
    while True:
        play_game()
        
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again != 'y':
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
