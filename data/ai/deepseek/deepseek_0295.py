import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # First N players

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')  # For Unix/Linux. Use 'cls' for Windows
    
    # Print column headers
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    
    # Print the bottom border
    print('+---' * COLS + '+')

def is_valid_column(board, col):
    if not (0 <= col < COLS):
        return False
    # Check if the topmost cell in the column is empty
    return board[0][col] == ' '

def drop_checker(board, col, checker):
    # Find the lowest empty row in the specified column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full (should not happen if checked with is_valid_column)

def check_win(board, row, col, checker):
    # Check horizontal, vertical, and both diagonals for 4 in a row
    
    # Directions: (dx, dy) pairs for horizontal, vertical, diagonal down, diagonal up
    directions = [
        [(0, 1), (0, -1)],  # Horizontal
        [(1, 0), (-1, 0)],  # Vertical
        [(1, 1), (-1, -1)],  # Diagonal down
        [(1, -1), (-1, 1)]   # Diagonal up
    ]
    
    for direction_pair in directions:
        count = 1  # The current checker counts as 1
        
        for dx, dy in direction_pair:
            x, y = row + dx, col + dy
            while 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == checker:
                count += 1
                x += dx
                y += dy
                if count == 4:
                    return True
        
    return False

def is_draw(board):
    # Check if the top row is completely filled
    return all(cell != ' ' for cell in board[0])

def get_valid_column_input(current_player):
    while True:
        try:
            col_input = input(f"Player {current_player}, please enter a column: ").upper()
            if len(col_input) != 1:
                print("Please enter a single letter.")
                continue
            
            col = ord(col_input) - ord('A')
            if 0 <= col < COLS:
                return col
            else:
                print(f"Column must be between A and {chr(ord('A') + COLS - 1)}.")
        except (ValueError, TypeError):
            print("Invalid input. Please enter a column letter (A-G).")

def play_game():
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYERS[current_player_index]
    
    print_board(board)
    
    while True:
        # Get valid column input from the current player
        col = get_valid_column_input(current_player)
        
        # Check if the column is valid (not full)
        if not is_valid_column(board, col):
            print(f"Column {chr(ord('A') + col)} is full. Player {current_player} loses their turn.")
        else:
            # Place the checker and get the row
            row = drop_checker(board, col, current_player)
            
            # Print the updated board
            print_board(board)
            
            # Check for a win
            if check_win(board, row, col, current_player):
                print(f"Player {current_player} won!")
                break
            
            # Check for a draw
            if is_draw(board):
                print("Game ended in a draw!")
                break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = PLAYERS[current_player_index]

if __name__ == "__main__":
    play_game()
