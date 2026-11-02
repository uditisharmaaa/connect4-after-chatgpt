import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """Display the game board with column labels."""
    os.system('clear')
    print('\n  ' + '   '.join(COLUMN_LABELS))
    print(' +' + '---+' * NUM_COLS)
    
    for row in board:
        print(' | ' + ' | '.join(row) + ' |')
        print(' +' + '---+' * NUM_COLS)
    print()


def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        user_input = input(f"Player {player}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").strip().upper()
        
        if user_input not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        
        col_index = COLUMN_LABELS.index(user_input)
        return col_index


def drop_piece(board, col, player):
    """Drop a piece in the specified column. Returns True if successful, False if column is full."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False


def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (down-left)
    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLS):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(NUM_COLS))


def play_game():
    """Main game loop."""
    board = create_board()
    active_players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\nWelcome to Connect 4!")
    print(f"Players: {', '.join(active_players)}")
    print(f"Starting player: {active_players[current_player_index]}")
    input("\nPress Enter to start...")
    
    while True:
        current_player = active_players[current_player_index]
        print_board(board)
        
        # Get valid move
        while True:
            col = get_column_input(current_player)
            if drop_piece(board, col, current_player):
                break
            print(f"Column {COLUMN_LABELS[col]} is full! Choose another column.")
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉\n")
            break
        
        # Check for draw
        if check_draw(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Main function to run the game with replay option."""
    while True:
        play_game()
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
