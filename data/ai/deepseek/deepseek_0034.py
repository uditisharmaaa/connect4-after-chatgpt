import os
import random

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# List of possible player checkers
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = '  '
    for col in range(BOARD_COLS):
        header += f"{chr(65 + col)}   "  # 65 is ASCII for 'A'
    print(header.rstrip())
    
    # Print the board rows
    for row in range(BOARD_ROWS):
        print('+---+' * BOARD_COLS)
        print('|', end='')
        for col in range(BOARD_COLS):
            print(f' {board[row][col]} |', end='')
        print()
    print('+---+' * BOARD_COLS)

def get_valid_column(board):
    """Prompt the player for a column input and validate it."""
    while True:
        column = input("Player {}, please enter a column: ".format(current_player + 1)).upper()
        if len(column) != 1:
            print("Please enter a single letter.")
            continue
        col = ord(column) - ord('A')  # Convert letter to column index (0-based)
        if col < 0 or col >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        if board[0][col] != ' ':
            print("Column is already full. Please choose another column.")
            continue
        return col

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full (should not happen if validated earlier)

def check_win(board, player_row, player_col, checker):
    """Check if the current move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down
        (1, -1)   # diagonal up
    ]
    
    for dr, dc in directions:
        count = 1  # The current checker
        
        # Check in the positive direction
        r, c = player_row + dr, player_col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS:
            if board[r][c] == checker:
                count += 1
                r += dr
                c += dc
            else:
                break
        
        # Check in the negative direction
        r, c = player_row - dr, player_col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS:
            if board[r][c] == checker:
                count += 1
                r -= dr
                c -= dc
            else:
                break
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    global current_player
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    clear_screen()
    print("Connect 4 Game")
    print_board(board)
    
    while True:
        print(f"Player {current_player + 1}'s turn ({player_checkers[current_player]})")
        col = get_valid_column(board)
        row = place_checker(board, col, player_checkers[current_player])
        
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            break
        elif is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
