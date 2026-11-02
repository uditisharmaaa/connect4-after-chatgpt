import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Clear the screen before printing the board
    os.system('clear')
    
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + ('---+' * COLS))

def is_valid_move(board, col):
    """Check if a move is valid (column is not full)."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def drop_checker(board, col, checker):
    """Drop a checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return

def check_win(board, checker):
    """Check if the specified checker has won."""
    # Check horizontal, vertical, and diagonal wins
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + dr * i, col + dc * i
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def get_player_move(player):
    """Get a valid column choice from the player."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha() or ord(col_input) < 65 or ord(col_input) >= 65 + COLS:
            print(f"Invalid input. Please enter a column letter from A to {chr(65 + COLS - 1)}.")
            continue
        col = ord(col_input) - 65
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        return col

def play_game():
    """Main game loop."""
    current_player = random.choice(PLAYERS)
    print(f"Player {current_player} starts first!")
    
    while True:
        print_board(board)
        col = get_player_move(current_player)
        drop_checker(board, col, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

# Initialize the board
board = initialize_board()

# Start the game
play_game()
