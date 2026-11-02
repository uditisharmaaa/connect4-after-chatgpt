import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)])
    print(header)
    
    # Print each row with borders
    for row in board:
        border = '+' + ('---+' * COLS)
        print(border)
        row_str = '| ' + ' | '.join(cell for cell in row) + ' |'
        print(row_str)
    
    # Print bottom border
    print('+' + ('---+' * COLS))

def get_valid_move(player, board):
    """Prompt the player for a valid move and return the column index."""
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        
        # Check for valid column letter
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if the column is full
        if board[0][col] != ' ':
            print("That column is full. Please choose another.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full (shouldn't happen due to prior validation)

def check_win(board, row, col, checker):
    """Check if placing a checker at (row, col) results in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down
        (1, -1)   # diagonal up
    ]
    
    for dr, dc in directions:
        count = 1  # current checker
        
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        col = get_valid_move(current_player, board)
        row = place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    play_game()
