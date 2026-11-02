import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Player symbols in order (max 5 players)
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)) + '  '
    print(header)
    
    # Print the board rows with borders
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        # Create the row with checks or spaces
        row_str = '|'
        for cell in row:
            row_str += ' ' + cell + ' |'
        print(row_str)
    print(border)

def get_valid_column(player, board):
    """Prompt the player for a column and validate the input."""
    while True:
        col_input = input(f"Player {player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(65 + BOARD_COLS - 1))
            continue
        
        col = ord(col_input) - ord('A')
        if col < 0 or col >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}")
            continue
        
        # Check if column is full
        if board[0][col] != ' ':
            print("That column is full. Please choose another.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_winner(board, row, col, player):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    players = PLAYERS[:NUM_PLAYERS]
    
    while True:
        os.system('clear')
        print_board(board)
        player = players[current_player_idx]
        col = get_valid_column(player, board)
        row = place_checker(board, col, player)
        
        if check_winner(board, row, col, player):
            os.system('clear')
            print_board(board)
            print(f"Player {player} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
