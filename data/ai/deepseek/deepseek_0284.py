import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with whitespaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the board with the current state."""
    os.system('clear')
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    # Print board rows
    for row in board:
        print('+---+' * BOARD_COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---+' * BOARD_COLS)

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        if board[0][col_num] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_num

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col
    return None  # Column is full (shouldn't happen due to validation)

def check_win(board, row, col, player):
    """Check if the current move results in a win."""
    # Check horizontal
    for c in range(max(0, col - 3), min(col + 1, BOARD_COLS - 3)):
        if all(board[row][c + i] == player for i in range(4)):
            return True
    # Check vertical
    for r in range(max(0, row - 3), min(row + 1, BOARD_ROWS - 3)):
        if all(board[r + i][col] == player for i in range(4)):
            return True
    # Check diagonal (top-left to bottom-right)
    for r, c in zip(range(max(0, row - 3), min(row + 1, BOARD_ROWS - 3)),
                    range(max(0, col - 3), min(col + 1, BOARD_COLS - 3))):
        if all(board[r + i][c + i] == player for i in range(4)):
            return True
    # Check diagonal (bottom-left to top-right)
    for r, c in zip(range(min(BOARD_ROWS - 1, row + 3), max(row - 1, 2), -1),
                    range(max(0, col - 3), min(col + 1, BOARD_COLS - 3))):
        if all(board[r - i][c + i] == player for i in range(4)):
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    global current_player
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row, _ = place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
