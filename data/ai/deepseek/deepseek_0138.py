import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First N players based on NUM_PLAYERS

def initialize_board():
    """Create and return an empty board with dimensions NUM_ROWS x NUM_COLS."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column letters (A, B, etc.)
    print('  ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print the board rows with separators
    for row in board:
        print('+---+' * NUM_COLS)
        formatted_row = '|' + '|'.join(f' {cell} ' for cell in row) + '|'
        print(formatted_row)
    
    # Print the bottom border
    print('+---+' * NUM_COLS)

def is_valid_move(column, board):
    """Check if placing a checker in the specified column is valid."""
    if not column.isalpha() or len(column) != 1:
        return False
    
    col_index = ord(column.upper()) - ord('A')
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if there's at least one empty space in the column
    return board[0][col_index] == ' '

def drop_checker(board, column, checker):
    """Drop the checker into the specified column and return the row where it lands."""
    col_index = ord(column.upper()) - ord('A')
    
    # Find the lowest empty row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    
    return -1  # This line should never be reached if move is valid

def check_win(board, row, col, checker):
    """Check if the recent move at (row, col) caused a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # The current checker is already placed
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != ' ' for row in board for cell in row)

def get_player_move(player, board):
    """Prompt the player for a valid column and return it."""
    while True:
        column = input(f"Player {player}, please enter a column: ").strip()
        if is_valid_move(column, board):
            return column.upper()
        print("Invalid move. Please try again.")

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        
        column = get_player_move(current_player, board)
        row = drop_checker(board, column, current_player)
        
        if check_win(board, row, ord(column) - ord('A'), current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
