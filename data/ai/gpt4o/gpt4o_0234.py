import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

# Initialize board with spaces
board = [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

def print_board():
    """Prints the current state of the board."""
    # Clear the terminal screen
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(BOARD_COLUMNS)))
    print('+' + '---+' * BOARD_COLUMNS)

    # Print each row
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+' + '---+' * BOARD_COLUMNS)

def place_checker(column, checker):
    """Places a checker in the specified column."""
    # Place checker in the lowest empty space in the column
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def is_valid_input(input_column):
    """Checks if the user's input is valid."""
    if len(input_column) != 1 or not input_column.isalpha():
        return False
    
    column_index = ord(input_column.upper()) - ord('A')
    if column_index < 0 or column_index >= BOARD_COLUMNS:
        return False
    
    if board[0][column_index] != ' ':
        return False
    
    return True

def check_winner():
    """Checks for a winning configuration in the board."""
    # Check horizontal, vertical, and diagonal wins
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLUMNS):
            if board[r][c] == ' ':
                continue

            # Check horizontal win
            if c <= BOARD_COLUMNS - 4 and all(board[r][c+i] == board[r][c] for i in range(4)):
                return True
            
            # Check vertical win
            if r <= BOARD_ROWS - 4 and all(board[r+i][c] == board[r][c] for i in range(4)):
                return True
            
            # Check diagonal win (bottom left to top right)
            if r <= BOARD_ROWS - 4 and c <= BOARD_COLUMNS - 4 and all(board[r+i][c+i] == board[r][c] for i in range(4)):
                return True
            
            # Check diagonal win (top left to bottom right)
            if r >= 3 and c <= BOARD_COLUMNS - 4 and all(board[r-i][c+i] == board[r][c] for i in range(4)):
                return True
    
    return False

def check_draw():
    """Checks if the board is completely filled."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Select random starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    # Print initial board
    print_board()
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        
        input_column = input().strip().upper()
        
        if not is_valid_input(input_column):
            print("Invalid input. Try again.")
            continue
        
        # Convert column letter to index
        column_index = ord(input_column) - ord('A')
        
        place_checker(column_index, CHECKERS[current_player])
        print_board()
        
        # Check for a winner
        if check_winner():
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for a draw
        if check_draw():
            print("The game is a draw!")
            break
        
        # Alternate player turns
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
