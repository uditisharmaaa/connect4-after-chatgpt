import os
import random

# Constants for board dimensions and number of players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checker symbols for up to 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with whitespaces."""
    board = []
    for _ in range(NUM_ROWS):
        row = [' ' for _ in range(NUM_COLS)]
        board.append(row)
    return board

def print_board(board):
    """Print the current state of the board with column labels."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    
    # Print the board with borders
    for row in board:
        print('+---+' * NUM_COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * NUM_COLS)

def get_valid_column(current_player):
    """
    Prompt the player to enter a valid column.
    Keep asking until a valid input is provided.
    """
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single uppercase letter.")
            continue
        col = ord(col_input) - ord('A')
        if 0 <= col < NUM_COLS:
            return col
        else:
            print(f"Invalid column. Please choose between A and {chr(ord('A') + NUM_COLS - 1)}.")

def place_checker(board, col, checker):
    """
    Place the checker in the lowest available row of the specified column.
    Return the row where the checker was placed, or -1 if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the recent move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = players[current_player_index]
    
    print_board(board)
    
    while True:
        col = get_valid_column(current_player)
        row = place_checker(board, col, current_player)
        
        if row == -1:
            print("Column is full. You lose your turn.")
        else:
            print_board(board)
            if check_win(board, row, col, current_player):
                print(f"Player {current_player} won!")
                break
            if is_board_full(board):
                print("Game ended in a draw!")
                break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = players[current_player_index]

if __name__ == "__main__":
    main()
