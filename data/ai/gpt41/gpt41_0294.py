import os
import random
import string

# ----- CONSTANTS -----
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2     # Set to 2 for submission (can be set to 2-5 for testing and extension)
WIN_COUNT = 4

# ----- FUNCTIONS -----

def clear_screen():
    """Clear the game screen"""
    os.system('clear')  # Use 'cls' for Windows

def create_board(rows, cols):
    """Initialize the Connect 4 board with whitespaces."""
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """Display the board, with column headers (A, B, C, ...) and formatted borders."""
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)

    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_input(board, current_player):
    """Prompt the current player for valid column input."""
    cols = len(board[0])
    while True:
        choice = input(f"Player {current_player}, please enter a column: ")
        choice = choice.strip().upper()
        if len(choice) != 1 or choice not in string.ascii_uppercase[:cols]:
            print("Invalid input. Please select a column A to", string.ascii_uppercase[cols-1])
            continue
        col_index = ord(choice) - ord('A')
        # Check if column is full
        if board[0][col_index] != ' ':
            print("Column is full. You lose your turn.")
            return None  # Lose the turn
        return col_index

def place_checker(board, col, symbol):
    """Place the player's symbol in the lowest available row in the selected column."""
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col  # Return position where checker was placed
    # Should not reach here if checked before
    return None

def check_direction(board, row, col, delta_row, delta_col, symbol):
    """Check WIN_COUNT checkers in a particular direction from (row, col)."""
    count = 0
    r, c = row, col
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, symbol):
    """Check all directions for a win condition."""
    # Directions: (delta_row, delta_col)
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # horizontal, vertical, diag-down, diag-up
    for dr, dc in directions:
        count = 1  # current piece
        # Check in positive direction
        count += check_direction(board, row+dr, col+dc, dr, dc, symbol)
        # Check in negative (opposite) direction
        count += check_direction(board, row-dr, col-dc, -dr, -dc, symbol)
        if count >= WIN_COUNT:
            return True
    return False

def board_is_full(board):
    """Returns True if the board has no empty spaces left."""
    return all(cell != ' ' for cell in board[0])

def main():
    # Initialize
    board = create_board(ROWS, COLUMNS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select starting player (index)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    clear_screen()
    print_board(board)
    print(f"Player {player_symbols[current_player_idx]} starts.\n")
    
    move_count = 0
    winner = None
    while True:
        player_symbol = player_symbols[current_player_idx]
        col_index = get_valid_input(board, player_symbol)
        
        clear_screen()
        if col_index is not None:
            # Place checker
            row_index, _ = place_checker(board, col_index, player_symbol)
            move_count += 1
            print_board(board)
            
            # Check win
            if check_win(board, row_index, col_index, player_symbol):
                print(f"Player {player_symbol} won!")
                break
            # Check draw
            if board_is_full(board):
                print("It's a draw!")
                break
        else:
            print_board(board)
        
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
