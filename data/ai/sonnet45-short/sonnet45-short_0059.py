import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2-5 for different number of players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Display the game board."""
    os.system('clear')
    print("\n  " + "   ".join(COLUMN_LABELS))
    print("  " + "---" * COLS)
    
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("  " + "---" * COLS)
    print()


def is_valid_move(board, col):
    """Check if a move is valid (column not full)."""
    return board[0][col] == ' '


def get_next_open_row(board, col):
    """Find the lowest empty row in a column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None


def drop_piece(board, row, col, symbol):
    """Place a piece on the board."""
    board[row][col] = symbol


def check_win(board, symbol):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True
    
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True
    
    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and
                board[row - 1][col + 1] == symbol and
                board[row - 2][col + 2] == symbol and
                board[row - 3][col + 3] == symbol):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True


def get_player_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player_symbol}, choose a column (A-G): ").strip().upper()
        
        if len(move) != 1 or move not in COLUMN_LABELS:
            print(f"Invalid input! Please enter a letter from A to G.")
            continue
        
        col_index = COLUMN_LABELS.index(move)
        
        if not is_valid_move(board, col_index):
            print(f"Column {move} is full! Choose another column.")
            continue
        
        return col_index


def play_game():
    """Main game loop."""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Welcome to Connect 4!")
    print(f"Players: {', '.join(players)}")
    print(f"Player {players[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    game_over = False
    
    while not game_over:
        print_board(board)
        current_symbol = players[current_player_index]
        
        col = get_player_move(board, current_symbol)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_symbol)
        
        if check_win(board, current_symbol):
            print_board(board)
            print(f"🎉 Player {current_symbol} wins! 🎉")
            game_over = True
        elif is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Start the game."""
    play_game()
    
    while True:
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again == 'y':
            play_game()
        elif play_again == 'n':
            print("Thanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
