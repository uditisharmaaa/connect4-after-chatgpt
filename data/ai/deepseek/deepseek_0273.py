import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYER_COUNT = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

def initialize_board():
    """Initialize an empty game board with the given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    print(' ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print each row with separators
    for row in board:
        print('+' + '---+' * BOARD_COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print bottom border
    print('+' + '---+' * BOARD_COLS)

def get_valid_column(board):
    """Prompt the player for a valid column input."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        if board[0][col] != ' ':
            print("That column is already full. Choose another one.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return
    return None  # Column is full (shouldn't happen since we checked)

def check_win(board, player):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (all spaces filled)."""
    return all(cell != ' ' for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

# Main game loop
def play_game():
    """Run the Connect 4 game."""
    board = initialize_board()
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    global current_player
    current_player = PLAYERS[current_player_idx]
    
    while True:
        clear_screen()
        print_board(board)
        
        col = get_valid_column(board)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT
        current_player = PLAYERS[current_player_idx]

if __name__ == "__main__":
    play_game()
