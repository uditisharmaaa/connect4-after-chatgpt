import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board with columns labeled A, B, C, etc."""
    os.system('clear')
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLS)]))
    # Print the board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def is_valid_column(col, board):
    """Check if a column is valid and not full."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '  # Check if top cell is empty

def place_checker(col, player, board):
    """Place the player's checker in the specified column."""
    for row in range(ROWS-1, -1, -1):  # Start from bottom
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the player has won the game."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 0
                    for i in range(4):
                        r, c = row + i*dr, col + i*dc
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count == 4:
                        return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for cell in board[0])  # Check if top row is full

def get_player_input(board, player):
    """Get and validate player input for column choice."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(col_input) - ord('A')
        if not is_valid_column(col, board):
            print("Invalid column or column is full. Please try again.")
            continue
        return col

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_player_input(board, current_player)
        place_checker(col, current_player, board)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
