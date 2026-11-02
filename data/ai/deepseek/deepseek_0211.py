import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize an empty game board with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers (A, B, C, ...)
    headers = ['  ' + chr(65 + i) + ' ' for i in range(BOARD_COLS)]
    print(''.join(headers))
    
    # Print the board rows
    for row in board:
        row_str = '|' + '|'.join([f' {cell} ' for cell in row]) + '|'
        border = '+' + ('---+' * BOARD_COLS)
        print(border)
        print(row_str)
    
    # Print the bottom border
    print('+' + ('---+' * BOARD_COLS))

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not col_input or len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        if board[0][col] != ' ':
            print("Column is full. Choose another column.")
            continue
        
        return col

def place_checker(board, col, symbol):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Include the current cell
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for cell in board[0])

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main function to run the Connect 4 game."""
    global current_player
    
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        
        print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn.")
        col = get_valid_column(board)
        
        for row in range(BOARD_ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = PLAYER_SYMBOLS[current_player]
                
                if check_win(board, row, col, PLAYER_SYMBOLS[current_player]):
                    clear_screen()
                    print_board(board)
                    print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
                    return
                
                break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game ended in a draw!")
            return
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
