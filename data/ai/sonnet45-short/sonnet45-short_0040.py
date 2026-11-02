# Connect 4 Game
# Introduction to Computer Science Project

import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
COLUMN_LABELS = 'ABCDEFG'

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    os.system('clear')
    print('\n  Connect 4 Game')
    print('  ' + '   '.join(COLUMN_LABELS))
    print('  ' + '---' * COLS)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('  ' + '---' * COLS)
    print()

def is_valid_move(board, col):
    """Check if a column has space for a piece."""
    return 0 <= col < COLS and board[0][col] == ' '

def drop_piece(board, col, player):
    """Drop a piece in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def get_player_move(board, player):
    """Get and validate player input."""
    while True:
        move = input(f"Player {player}, enter column (A-G): ").upper().strip()
        
        if len(move) != 1 or move not in COLUMN_LABELS:
            print("Invalid input! Please enter a letter A-G.")
            continue
        
        col = COLUMN_LABELS.index(move)
        
        if not is_valid_move(board, col):
            print("Column is full! Choose another column.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Players: {', '.join(PLAYERS)}")
    print(f"Starting player: {PLAYERS[current_player_idx]}")
    input("Press Enter to start...")
    
    while True:
        current_player = PLAYERS[current_player_idx]
        print_board(board)
        
        col = get_player_move(board, current_player)
        row = drop_piece(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉")
            break
        
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

def main():
    """Entry point of the program."""
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").lower().strip()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
