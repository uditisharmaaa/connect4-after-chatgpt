import os
import random

# Global constants for board dimensions and players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def initialize_board():
    """
    Initialize the game board with all empty cells (spaces).
    Returns a 2D list representing the board.
    """
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print('  ', end='')
    for col in range(COLUMNS):
        print(f'{chr(65 + col)}   ', end='')
    print()
    
    # Print top border
    print('+---' * COLUMNS + '+')
    
    # Print each row
    for row in board:
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
        print('+---' * COLUMNS + '+')

def get_valid_column_input(current_player):
    """
    Get valid column input from the player.
    Keep asking until a valid input is provided.
    Returns the column index (0-based).
    """
    while True:
        user_input = input(f'Player {PLAYER_CHECKERS[current_player]}, please enter a column: ').strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print('Invalid input. Please enter a single letter.')
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print('Invalid input. Please enter a letter.')
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board dimensions
        if col_index < 0 or col_index >= COLUMNS:
            print(f'Invalid column. Please enter a letter from A to {chr(65 + COLUMNS - 1)}.')
            continue
        
        return col_index

def place_checker(board, col_index, current_player):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if placement was successful, False if column is full.
    """
    # Find the lowest empty row in the specified column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = PLAYER_CHECKERS[current_player]
            return True
    
    # Column is full
    print('That column is full. Please choose another column.')
    return False

def check_win(board, row, col, current_player):
    """
    Check if the current player has won by placing a checker at (row, col).
    Check horizontally, vertically, and both diagonals.
    Returns True if there are 4 in a row, False otherwise.
    """
    checker = PLAYER_CHECKERS[current_player]
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < COLUMNS and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLUMNS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False

def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if all cells are occupied, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def play_game():
    """
    Main game loop that handles the Connect 4 game flow.
    """
    # Initialize board
    board = initialize_board()
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get valid column input from current player
        while True:
            col_index = get_valid_column_input(current_player)
            # Try to place the checker
            if place_checker(board, col_index, current_player):
                # Find the row where the checker was placed
                placed_row = -1
                for row in range(ROWS):
                    if board[row][col_index] == PLAYER_CHECKERS[current_player]:
                        placed_row = row
                        break
                
                # Print updated board
                print_board(board)
                
                # Check for win
                if check_win(board, placed_row, col_index, current_player):
                    print(f'Player {PLAYER_CHECKERS[current_player]} won!')
                    game_over = True
                    break
                
                # Check for draw
                if is_board_full(board):
                    print('It\'s a draw!')
                    game_over = True
                    break
                
                # Move to next player
                current_player = (current_player + 1) % NUM_PLAYERS
                break

def main():
    """
    Entry point of the program.
    """
    play_game()

if __name__ == '__main__':
    main()
