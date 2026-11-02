import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a new empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + ('---+' * COLS))
    for row in board:
        # Print each row with separators
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def get_valid_column(board):
    """Prompt the player for a column until a valid one is provided."""
    while True:
        choice = input(f"Player {current_player}, please enter a column: ").upper()
        if len(choice) != 1 or not choice.isalpha():
            print("Please enter a single letter (A-G).")
            continue
        col = ord(choice) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col] != ' ':
            print("This column is full. Choose another one.")
            continue
        return col

def drop_checker(board, col, checker):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the current move resulted in a win."""
    # Check horizontal
    count = 1
    # Left
    for c in range(col - 1, max(col - 4, -1), -1):
        if board[row][c] == checker:
            count += 1
        else:
            break
    # Right
    for c in range(col + 1, min(col + 4, COLS)):
        if board[row][c] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check vertical
    count = 1
    # Down (since we drop from top)
    for r in range(row + 1, min(row + 4, ROWS)):
        if board[r][col] == checker:
            count += 1
        else:
            break
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    # Top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Bottom-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    count = 1
    # Top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Bottom-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]
    
    while True:
        print_board(board)
        col = get_valid_column(board)
        row = drop_checker(board, col, checkers[current_player])
        
        if check_win(board, row, col, checkers[current_player]):
            print_board(board)
            print(f"Player {checkers[current_player]} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
