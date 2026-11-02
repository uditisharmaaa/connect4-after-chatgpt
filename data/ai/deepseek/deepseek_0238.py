import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column letters
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or col < 'A' or col > chr(ord('A') + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + COLS - 1)}.")
            continue
        
        col_index = ord(col) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Choose another column.")
            continue
        
        return col_index

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return (row, col)
    return None

def check_win(board, row, col, player):
    """Check if the current move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS[:NUM_PLAYERS])
    
    while True:
        print_board(board)
        col = get_valid_column(board)
        row, col = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_player_index + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
