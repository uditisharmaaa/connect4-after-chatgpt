import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only take required players

def create_board():
    """Create and initialize an empty board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print top border
    print('+' + '---+' * BOARD_COLS)
    
    # Print each row with borders
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * BOARD_COLS)

def get_valid_column(board):
    """Prompt the current player for a column and validate the input."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(65 + BOARD_COLS - 1))
            continue
        
        col_num = ord(col) - ord('A')
        if not 0 <= col_num < BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        if board[0][col_num] != ' ':
            print("Column is full. Choose another column.")
            continue
        
        return col_num

def place_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    player = board[row][col]
    
    # Check horizontal
    count = 1
    for c in range(col + 1, BOARD_COLS):
        if board[row][c] != player:
            break
        count += 1
    for c in range(col - 1, -1, -1):
        if board[row][c] != player:
            break
        count += 1
    if count >= 4:
        return True
    
    # Check vertical
    count = 1
    for r in range(row + 1, BOARD_ROWS):
        if board[r][col] != player:
            break
        count += 1
    for r in range(row - 1, -1, -1):
        if board[r][col] != player:
            break
        count += 1
    if count >= 4:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    r, c = row + 1, col + 1
    while r < BOARD_ROWS and c < BOARD_COLS and board[r][c] == player:
        count += 1
        r += 1
        c += 1
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == player:
        count += 1
        r -= 1
        c -= 1
    if count >= 4:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    r, c = row + 1, col - 1
    while r < BOARD_ROWS and c >= 0 and board[r][c] == player:
        count += 1
        r += 1
        c -= 1
    r, c = row - 1, col + 1
    while r >= 0 and c < BOARD_COLS and board[r][c] == player:
        count += 1
        r -= 1
        c += 1
    if count >= 4:
        return True
    
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main game loop."""
    global current_player
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        col = get_valid_column(board)
        for row in range(BOARD_ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = current_player
                if check_win(board, row, col):
                    os.system('clear')
                    print_board(board)
                    print(f"Player {current_player} won!")
                    return
                break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw.")
            return
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
