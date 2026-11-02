import random
import os

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board"""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print each row with borders
    for row in board:
        print("+" + "---+" * COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column(col_letter):
    """Check if the column input is valid"""
    if len(col_letter) != 1:
        return False
    if not col_letter.isalpha():
        return False
    col_index = ord(col_letter.upper()) - 65
    return 0 <= col_index < COLS

def get_column_index(col_letter):
    """Convert column letter to index"""
    return ord(col_letter.upper()) - 65

def is_column_full(board, col_index):
    """Check if a column is full"""
    return board[0][col_index] != " "

def place_checker(board, col_index, symbol):
    """Place a checker in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win"""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full"""
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def get_player_move(board, player_symbol):
    """Get and validate player input"""
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ")
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(col_input)
        
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            return None
        
        return col_index

def main():
    """Main game loop"""
    # Initialize board
    board = create_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        player_symbol = PLAYER_SYMBOLS[current_player]
        
        # Get player move
        col_index = get_player_move(board, player_symbol)
        
        if col_index is not None:
            # Place checker
            row = place_checker(board, col_index, player_symbol)
            
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_win(board, row, col_index, player_symbol):
                print(f"Player {player_symbol} won!")
                game_over = True
            # Check for draw
            elif is_board_full(board):
                print("The game is a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player = (current_player + 1) % NUM_PLAYERS
        else:
            # Player loses turn due to full column
            print_board(board)
            current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
