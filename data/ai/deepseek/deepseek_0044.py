import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and separators."""
    os.system('clear')
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + '---+' * COLS)
    
    for row in board:
        # Print row content
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row separator
        print('+' + '---+' * COLS)

def get_valid_column(player, board):
    """Prompt the player for a column and validate the input."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            if len(col_input) != 1 or not col_input.isalpha():
                raise ValueError("Invalid input. Please enter a single letter.")
            
            col = ord(col_input) - ord('A')
            if col < 0 or col >= COLS:
                raise ValueError("Column out of range.")
            
            if board[0][col] != ' ':
                raise ValueError("Column is full. Please choose another column.")
            
            return col
        except ValueError as e:
            print(e)

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the player has won after placing a checker."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal (top-left to bottom-right)
        (1, -1)  # Diagonal (top-right to bottom-left)
    ]
    
    for dr, dc in directions:
        count = 1
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        # Check win condition
        if count >= 4:
            return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(current_player, board)
        row = place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
