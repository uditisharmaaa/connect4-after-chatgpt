import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First NUM_PLAYERS symbols

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    # Print column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_random_first_player():
    """Return a random player to start the game."""
    return random.choice(PLAYERS)

def get_valid_input(current_player):
    """Get and validate player input."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col_idx = ord(column) - ord('A')
        if 0 <= col_idx < COLS:
            return col_idx
        print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")

def place_checker(board, col_idx, current_player):
    """Place the checker in the lowest empty row of the column."""
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = current_player
            return True
    return False  # Column is full

def check_win(board, row, col, current_player):
    """Check if the current move results in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == current_player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == current_player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = get_random_first_player()
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        col_idx = get_valid_input(current_player)
        if not place_checker(board, col_idx, current_player):
            print("Column is full. You lose your turn.")
        else:
            # Find the row where the checker was placed
            for row_idx in range(ROWS):
                if board[row_idx][col_idx] == current_player:
                    break
            if check_win(board, row_idx, col_idx, current_player):
                clear_screen()
                print_board(board)
                print(f"Player {current_player} won!")
                return
        
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            return
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
