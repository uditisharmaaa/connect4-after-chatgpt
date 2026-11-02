import random
import os

# Constants
NUM_ROWS = 6
NUM_COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change this to 2-5 for different player counts
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  A   B   C   D   E   F   G')
    print(' ' + '---' * NUM_COLS + '--')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print(' ' + '---' * NUM_COLS + '--')
    print()

def get_column_input(player):
    """Get and validate column input from player."""
    while True:
        choice = input(f"Player {player}, choose a column (A-G): ").upper().strip()
        if choice in COLUMNS:
            return COLUMNS.index(choice)
        else:
            print("Invalid input! Please enter a letter from A to G.")

def drop_piece(board, col, player):
    """Drop a piece in the specified column. Returns True if successful."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def is_column_full(board, col):
    """Check if a column is full."""
    return board[0][col] != ' '

def check_win(board, player):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and
                board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\n*** Connect 4 - {NUM_PLAYERS} Players ***")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!\n")
    input("Press Enter to start...")
    
    while True:
        current_player = players[current_player_index]
        print_board(board)
        
        # Get valid move
        while True:
            col = get_column_input(current_player)
            if is_column_full(board, col):
                print("That column is full! Choose another column.")
            else:
                break
        
        # Drop the piece
        drop_piece(board, col, current_player)
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    while True:
        play_game()
        again = input("Play again? (y/n): ").lower().strip()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
