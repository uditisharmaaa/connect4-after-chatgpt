import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    
    # Print the board
    border = "+" + ("---+" * COLS)
    print(border)
    for row in board:
        print("| " + " | ".join(cell for cell in row) + " |")
        print(border)

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if not col.isalpha() or len(col) != 1:
        return False
    
    col_index = ord(col.upper()) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    
    return board[0][col_index] == " "

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the column."""
    col_index = ord(col.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return (row, col_index)
    return None

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),  # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for cell in board[0])

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]
    
    print_board(board)
    print(f"Player {checkers[current_player]} starts the game!")
    
    while True:
        player_checker = checkers[current_player]
        col = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if not is_valid_column(col, board):
            print("Invalid column. Please try again.")
            continue
        
        row, col_placed = place_checker(board, col, player_checker)
        col_index = ord(col.upper()) - ord('A')
        print_board(board)
        
        if check_win(board, row, col_index, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
