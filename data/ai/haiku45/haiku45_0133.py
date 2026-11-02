import os
import random

# Game constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create an empty board with given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current board state."""
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print('  ', end='')
    for col in range(cols):
        print(f'{chr(65 + col)}   ', end='')
    print()
    
    # Print board with borders
    for row in range(rows):
        print('+---' * cols + '+')
        print('|', end='')
        for col in range(cols):
            print(f' {board[row][col]} |', end='')
        print()
    print('+---' * cols + '+')

def is_valid_move(board, col):
    """Check if a move is valid (column exists and has space)."""
    if col < 0 or col >= len(board[0]):
        return False
    return board[0][col] == ' '

def place_checker(board, col, checker):
    """Place a checker in the given column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last placed checker resulted in a win."""
    rows, cols = len(board), len(board[0])
    
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw)."""
    return all(board[0][col] != ' ' for col in range(len(board[0])))

def get_player_move(board, player):
    """Get and validate player input."""
    cols = len(board[0])
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if move < 'A' or move >= chr(65 + cols):
            print(f"Invalid column. Please enter a letter from A to {chr(64 + cols)}.")
            continue
        
        col = ord(move) - 65
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = checkers[current_player]
        
        # Get player move
        col = get_player_move(board, player_checker)
        
        # Place checker
        row = place_checker(board, col, player_checker)
        
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
