import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create an empty board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    for row in board:
        # Print row with cells
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def is_valid_column(col, board):
    """Check if the column is valid and has space."""
    if not col.isalpha() or len(col) != 1:
        return False
    col_idx = ord(col.upper()) - ord('A')
    if col_idx < 0 or col_idx >= COLS:
        return False
    return board[0][col_idx] == ' '

def place_checker(board, col, player):
    """Place player's checker in the specified column."""
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = player
            return row_idx, col_idx
    return -1, -1  # Column is full (shouldn't happen due to validation)

def check_win(board, row, col, player):
    """Check if the player has won after placing a checker at (row, col)."""
    # Check horizontally
    count = 1
    # Left
    for c in range(col - 1, -1, -1):
        if board[row][c] == player:
            count += 1
        else:
            break
    # Right
    for c in range(col + 1, COLS):
        if board[row][c] == player:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check vertically
    count = 1
    # Down (only needed, since new piece is at topmost of column)
    for r in range(row + 1, ROWS):
        if board[r][col] == player:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == player:
            count += 1
            r -= 1
            c -= 1
        else:
            break
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS:
        if board[r][c] == player:
            count += 1
            r += 1
            c += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count += 1
            r -= 1
            c += 1
        else:
            break
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0:
        if board[r][c] == player:
            count += 1
            r += 1
            c -= 1
        else:
            break
    if count >= 4:
        return True

    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        clear_screen()
        print_board(board)
        
        # Check for draw before prompting input
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Get player input
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(col, board):
            continue
        
        # Place checker and check for win
        row, col_placed = place_checker(board, col, current_player)
        if check_win(board, row, col_placed, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
