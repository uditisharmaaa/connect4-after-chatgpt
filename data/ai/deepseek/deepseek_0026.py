import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def initialize_board():
    """Initialize an empty game board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print board borders and cells
    for row in board:
        print('+' + '---+' * COLS)  # Top border for each row
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')  # Cell content
    print('+' + '---+' * COLS)  # Bottom border

def get_player_move(current_player, valid_columns):
    """
    Prompt the current player for a column to drop their checker.
    Validate the input and ensure it is a valid column.
    """
    while True:
        move = input(f"Player {current_player}, please enter a column: ").upper()
        if len(move) != 1:
            print("Invalid input. Please enter a single uppercase letter (A, B, etc.).")
            continue
        if move not in valid_columns:
            print("Invalid column. Please choose a valid column (A, B, etc.).")
            continue
        return move

def drop_checker(board, col, player):
    """
    Place the player's checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if successful, False if the column is full.
    """
    col_idx = ord(col) - ord('A')  # Convert column letter to index (0-based)
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """
    Check if the current player has won the game by getting 4 in a row.
    Check horizontal, vertical, and both diagonals.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if check_win_from_position(board, row, col, player):
                return True
    return False

def check_win_from_position(board, row, col, player):
    """
    Check if the player has 4 in a row starting from a specific position.
    Check horizontal, vertical, and both diagonals.
    """
    # Directions: (drow, dcol) for horizontal, vertical, down-diag, up-diag
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for drow, dcol in directions:
        count = 0
        for step in range(4):
            r, c = row + step * drow, col + step * dcol
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        if count == 4:
            return True
    return False

def check_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def main():
    clear_screen()
    board = initialize_board()
    # Select a random starting player
    current_player = random.choice(PLAYERS[:NUM_PLAYERS])
    print("Starting player:", current_player)
    print_board(board)
    
    while True:
        valid_columns = [chr(ord('A') + i) for i in range(COLS)]
        col = get_player_move(current_player, valid_columns)
        
        if not drop_checker(board, col, current_player):
            print("Column is full. Try another column.")
            continue  # Player loses turn if column is full
        
        clear_screen()
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to the next player
        current_idx = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_idx + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
