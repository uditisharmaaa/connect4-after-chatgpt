import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

def initialize_board(rows, cols):
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing the board
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print the board rows
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def get_random_first_player(num_players):
    """Randomly select the first player."""
    return random.randint(0, num_players - 1)

def get_player_markers(num_players):
    """Return the list of player markers based on number of players."""
    markers = ['X', 'O', 'V', 'H', 'M']
    return markers[:num_players]

def is_valid_column(col, cols):
    """Check if the column input is valid."""
    if len(col) != 1:
        return False
    col_char = col.upper()
    return 'A' <= col_char <= chr(65 + cols - 1)

def place_checker(board, col, marker):
    """Place the marker in the specified column if possible."""
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = marker
            return True
    return False

def check_win(board, marker):
    """Check if the current player has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == marker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == marker for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == marker for i in range(4)):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == marker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    markers = get_player_markers(NUM_PLAYERS)
    current_player = get_random_first_player(NUM_PLAYERS)
    
    print("Starting Connect 4 Game!")
    print(f"Player {markers[current_player]} will go first.")
    
    while True:
        print_board(board)
        print(f"Player {markers[current_player]}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input, BOARD_COLS):
            print("Invalid column. Please enter a valid column letter (A-G).")
            continue
        
        if not place_checker(board, col_input, markers[current_player]):
            print("Column is full. Please try another column.")
            continue
        
        if check_win(board, markers[current_player]):
            print_board(board)
            print(f"Player {markers[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
