import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Display the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print the board with borders
    border = '+' + ('---+' * BOARD_COLS)
    print(border)
    
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print(border)

def is_valid_column(column):
    """Check if the column input is valid (A to corresponding max column letter)."""
    return len(column) == 1 and column.upper() in [chr(65 + i) for i in range(BOARD_COLS)]

def place_checker(board, column, checker):
    """Place the checker in the specified column at the lowest empty row."""
    col_index = ord(column.upper()) - ord('A')
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True  # Successfully placed
    return False  # Column is full

def check_win(board, checker):
    """Check if the current player has won."""
    # Directions: horizontal, vertical, diagonal-right, diagonal-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] != checker:
                continue
            for dr, dc in directions:
                count = 1
                for step in range(1, 4):
                    r, c = row + dr * step, col + dc * step
                    if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
    return False

def check_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        # Get player input
        column_input = input(f"Player {current_player}, please enter a column: ")
        
        # Validate input
        while not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter.")
            column_input = input(f"Player {current_player}, please enter a column: ")
        
        column = column_input.upper()
        
        # Place checker
        if place_checker(board, column, current_player):
            print_board(board)
            
            # Check for win
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            # Check for draw
            if check_draw(board):
                print("Game ended in a draw!")
                break
            
            # Switch to next player
            next_index = (PLAYERS.index(current_player) + 1) % NUM_PLAYERS
            current_player = PLAYERS[next_index]
        else:
            print(f"Column {column} is full. Player {current_player} loses turn.")
            next_index = (PLAYERS.index(current_player) + 1) % NUM_PLAYERS
            current_player = PLAYERS[next_index]

if __name__ == "__main__":
    main()
