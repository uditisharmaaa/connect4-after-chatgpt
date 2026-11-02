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
    print("\n  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_column(col_input):
    """Check if column input is valid (A-G)."""
    return col_input.upper() in COLUMN_LABELS

def get_column_index(col_input):
    """Convert column letter to index (0-6)."""
    return COLUMN_LABELS.index(col_input.upper())

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != ' '

def drop_piece(board, col_index, symbol):
    """Drop a piece in the specified column. Return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move created a winning condition."""
    
    # Check horizontal
    def check_direction(delta_row, delta_col):
        count = 1  # Count the piece just placed
        
        # Check in positive direction
        r, c = row + delta_row, col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += delta_row
            c += delta_col
        
        # Check in negative direction
        r, c = row - delta_row, col - delta_col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= delta_row
            c -= delta_col
        
        return count >= 4
    
    # Check all four directions: horizontal, vertical, diagonal /, diagonal \
    return (check_direction(0, 1) or   # Horizontal
            check_direction(1, 0) or   # Vertical
            check_direction(1, 1) or   # Diagonal \
            check_direction(1, -1))    # Diagonal /

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_valid_move(board, player_symbol):
    """Get and validate player input."""
    while True:
        col_input = input(f"Player {player_symbol}, enter column (A-G): ").strip()
        
        if not col_input:
            print("Error: Please enter a column letter.")
            continue
        
        if not is_valid_column(col_input):
            print("Error: Invalid column. Please enter A-G.")
            continue
        
        col_index = get_column_index(col_input)
        
        if is_column_full(board, col_index):
            print("Error: That column is full. Choose another.")
            continue
        
        return col_index

def get_number_of_players():
    """Get and validate the number of players."""
    while True:
        try:
            num_players = int(input(f"Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): "))
            if MIN_PLAYERS <= num_players <= MAX_PLAYERS:
                return num_players
            else:
                print(f"Error: Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        except ValueError:
            print("Error: Please enter a valid number.")

def play_game():
    """Main game loop."""
    # Setup
    os.system('clear')
    print("=" * 40)
    print("       WELCOME TO CONNECT 4!")
    print("=" * 40)
    print("\nConnect 4 pieces in a row to win!")
    print("(Horizontal, Vertical, or Diagonal)\n")
    
    num_players = get_number_of_players()
    players = PLAYER_SYMBOLS[:num_players]
    
    # Randomize starting player
    random.shuffle(players)
    
    board = create_board()
    current_player_index = 0
    move_count = 0
    
    print(f"\nPlayer order: {' -> '.join(players)}")
    print(f"Player {players[0]} goes first!")
    input("\nPress Enter to start...")
    
    # Game loop
    while True:
        os.system('clear')
        print_board(board)
        
        current_symbol = players[current_player_index]
        
        # Get valid move
        col_index = get_valid_move(board, current_symbol)
        
        # Drop piece
        row = drop_piece(board, col_index, current_symbol)
        move_count += 1
        
        # Clear and show updated board
        os.system('clear')
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_symbol):
            print("=" * 40)
            print(f"   PLAYER {current_symbol} WINS!")
            print("=" * 40)
            break
        
        # Check for draw
        if is_board_full(board):
            print("=" * 40)
            print("       IT'S A DRAW!")
            print("=" * 40)
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % num_players
    
    print(f"\nTotal moves: {move_count}")
    print("\nThanks for playing!")

def main():
    """Entry point of the program."""
    play_game()
    
    # Option to play again
    while True:
        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again == 'y':
            play_game()
        elif play_again == 'n':
            print("\nGoodbye!")
            break
        else:
            print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
