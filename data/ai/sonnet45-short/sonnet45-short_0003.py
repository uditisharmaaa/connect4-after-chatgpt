import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.
EMPTY = '.'


def create_board():
    """Create and return an empty game board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  ' + ' '.join(COLUMN_LABELS))
    print('  ' + '-' * (COLS * 2 - 1))
    for row in board:
        print('  ' + ' '.join(row))
    print()


def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").upper()
        
        if choice not in COLUMN_LABELS:
            print(f"Invalid input! Please choose a column from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        
        col_index = COLUMN_LABELS.index(choice)
        return col_index


def drop_piece(board, col, player):
    """
    Drop a piece in the specified column.
    Returns True if successful, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
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
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw)."""
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
        
        # Get valid move
        while True:
            col = get_column_input(current_player)
            if drop_piece(board, col, current_player):
                break
            print("That column is full! Choose another column.")
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % len(PLAYERS)


def main():
    """Run the game with option to play again."""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
