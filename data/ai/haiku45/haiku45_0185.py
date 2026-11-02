import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board(rows, cols):
    """Create and return an empty board with given dimensions."""
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board

def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        letter = chr(ord('A') + i)
        print(f" {letter}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")

def get_column_input(cols, board):
    """Get valid column input from player."""
    while True:
        col_letter = input("Player " + current_player + ", please enter a column: ").upper()
        
        # Check if input is a single letter
        if len(col_letter) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not col_letter.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(col_letter) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col_index, checker):
    """Place a checker in the specified column and return the row index."""
    # Find the lowest empty row in the column
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index
    return -1

def check_win(board, row, col, checker):
    """Check if there's a win at the current position."""
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, 1, -1):
        return True
    
    return False

def check_direction(board, row, col, checker, row_delta, col_delta):
    """Check if there are 4 checkers in a row in a given direction."""
    count = 1  # Count the current checker
    
    # Check in positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH

def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    global current_player
    
    board = initialize_board(ROWS, COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board, COLS)
    
    while True:
        current_player = player_checkers[current_player_index]
        
        # Get valid column input
        col_index = get_column_input(COLS, board)
        
        # Place the checker
        row_index = place_checker(board, col_index, current_player)
        
        # Print the updated board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, row_index, col_index, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    current_player = ""
    play_game()
