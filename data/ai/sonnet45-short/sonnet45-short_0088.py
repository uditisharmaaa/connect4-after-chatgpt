# Connect 4 Game
# An interactive Connect 4 game for 2-5 players

import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the current game board."""
    os.system('clear')
    print("\n  Connect 4  \n")
    
    # Print column labels
    print("  " + "   ".join(COLUMNS))
    print(" +" + "---+" * COLS)
    
    # Print rows (top to bottom)
    for row in board:
        print(" | " + " | ".join(row) + " |")
        print(" +" + "---+" * COLS)
    print()

def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    return board[0][col] == ' '

def get_next_row(board, col):
    """Find the next available row in a column (gravity effect)."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def drop_piece(board, col, player):
    """Drop a piece in the specified column for the current player."""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = player
        return True
    return False

def check_win(board, player):
    """Check if the current player has won."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row][col + 1] == player and
                board[row][col + 2] == player and
                board[row][col + 3] == player):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and
                board[row + 1][col] == player and
                board[row + 2][col] == player and
                board[row + 3][col] == player):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row - 1][col + 1] == player and
                board[row - 2][col + 2] == player and
                board[row - 3][col + 3] == player):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and
                board[row + 1][col + 1] == player and
                board[row + 2][col + 2] == player and
                board[row + 3][col + 3] == player):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player}, enter column (A-G): ").strip().upper()
        
        if len(move) != 1 or move not in COLUMNS:
            print("Invalid input! Please enter a letter from A to G.")
            input("Press Enter to continue...")
            continue
        
        col_index = COLUMNS.index(move)
        
        if not is_valid_move(board, col_index):
            print("Column is full! Choose another column.")
            input("Press Enter to continue...")
            continue
        
        return col_index

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Player {PLAYERS[current_player_index]} goes first!")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_index]
        print_board(board)
        
        col = get_player_move(board, current_player)
        drop_piece(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

def main():
    """Start the game."""
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(PLAYERS)}")
    input("Press Enter to begin...")
    
    play_game()
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
