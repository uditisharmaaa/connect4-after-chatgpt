import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board with columns labeled A, B, C, etc."""
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * len(board[0]))
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def is_valid_column(board, col):
    """Check if the column is valid and has space."""
    if col < 0 or col >= len(board[0]):
        return False
    # Check if top of column is empty
    return board[0][col] == ' '

def place_checker(board, col, symbol):
    """Place the checker in the lowest available row in the specified column."""
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col
    return -1, -1  # Shouldn't reach here if validated

def check_win(board, row, col, symbol):
    """Check if the last move caused a win (4 in a row horizontally, vertically, or diagonally)."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (no empty spaces left)."""
    return all(cell != ' ' for row in board for cell in row)

def get_column_input(player_symbol):
    """Get and validate column input from the player."""
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter from A to", chr(ord('A') + COLS - 1))
            continue
        col = ord(col_input) - ord('A')
        if 0 <= col < COLS:
            if is_valid_column(board, col):
                return col
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid column. Please enter a letter from A to", chr(ord('A') + COLS - 1))

def play_game():
    """Main game loop."""
    board = create_board(ROWS, COLS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        os.system('clear')
        print_board(board)
        
        col = get_column_input(current_player)
        row, _ = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    play_game()
