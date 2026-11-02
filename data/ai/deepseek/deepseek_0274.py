import os
import random

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Possible player checkers in order
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, cols):
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers (A, B, C, ...)
    headers = [chr(65 + i) for i in range(len(board[0]))]
    print('  ' + '   '.join(headers))
    
    # Print the top border
    print('+' + ('---+' * len(board[0])))
    
    for row in board:
        # Print each row with | as separators
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print the border after each row
        print('+' + ('---+' * len(board[0])))

def get_valid_column(board):
    """Prompt the player for a column input and validate it."""
    columns = [chr(65 + i) for i in range(len(board[0]))]
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if column not in columns:
            print(f"Invalid column. Please enter a letter from A to {chr(65 + len(board[0]) - 1)}.")
        else:
            col_index = ord(column) - ord('A')
            if board[0][col_index] != ' ':
                print("Column is full. Try another column.")
                continue
            return col_index

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col
    return None

def check_win(board, row, col, player):
    """Check if the current move resulted in a win."""
    # Check horizontal
    consecutive = 1
    # Left
    for c in range(col - 1, max(-1, col - 4), -1):
        if board[row][c] == player:
            consecutive += 1
        else:
            break
    # Right
    for c in range(col + 1, min(len(board[0]), col + 4)):
        if board[row][c] == player:
            consecutive += 1
        else:
            break
    if consecutive >= 4:
        return True

    # Check vertical
    consecutive = 1
    # Up (not needed since checkers fall down)
    # Down
    for r in range(row + 1, min(len(board), row + 4)):
        if board[r][col] == player:
            consecutive += 1
        else:
            break
    if consecutive >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    consecutive = 1
    # Top-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and consecutive < 4:
        if board[r][c] == player:
            consecutive += 1
            r -= 1
            c -= 1
        else:
            break
    # Bottom-right
    r, c = row + 1, col + 1
    while r < len(board) and c < len(board[0]) and consecutive < 4:
        if board[r][c] == player:
            consecutive += 1
            r += 1
            c += 1
        else:
            break
    if consecutive >= 4:
        return True

    # Check diagonal (top-right to bottom-left)
    consecutive = 1
    # Top-right
    r, c = row - 1, col + 1
    while r >= 0 and c < len(board[0]) and consecutive < 4:
        if board[r][c] == player:
            consecutive += 1
            r -= 1
            c += 1
        else:
            break
    # Bottom-left
    r, c = row + 1, col - 1
    while r < len(board) and c >= 0 and consecutive < 4:
        if board[r][c] == player:
            consecutive += 1
            r += 1
            c -= 1
        else:
            break
    if consecutive >= 4:
        return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def main():
    global current_player
    
    # Initialize the game
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    # Game loop
    while True:
        os.system('clear')
        print_board(board)
        
        # Get valid column input
        col = get_valid_column(board)
        
        # Place the checker
        pos = place_checker(board, col, current_player)
        
        # Check for win
        if check_win(board, pos[0], pos[1], current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
