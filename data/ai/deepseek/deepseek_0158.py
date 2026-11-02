import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print board rows with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def is_valid_move(col, board):
    """Check if a column is a valid move (not full and within bounds)."""
    if not (0 <= col < COLS):
        return False
    # Check if the top cell of the column is empty
    return board[0][col] == ' '

def make_move(col, symbol, board):
    """Place the symbol in the specified column at the lowest empty row."""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

def check_win(board, symbol):
    """Check if the current player has won."""
    # Check horizontal, vertical, and both diagonals
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and
                board[row][col] == symbol and
                board[row][col + 1] == symbol and
                board[row][col + 2] == symbol and
                board[row][col + 3] == symbol):
                return True  # Horizontal win
            
            if (row + 3 < ROWS and
                board[row][col] == symbol and
                board[row + 1][col] == symbol and
                board[row + 2][col] == symbol and
                board[row + 3][col] == symbol):
                return True  # Vertical win
            
            if (row + 3 < ROWS and col + 3 < COLS and
                board[row][col] == symbol and
                board[row + 1][col + 1] == symbol and
                board[row + 2][col + 2] == symbol and
                board[row + 3][col + 3] == symbol):
                return True  # Diagonal down-right win
            
            if (row + 3 < ROWS and col - 3 >= 0 and
                board[row][col] == symbol and
                board[row + 1][col - 1] == symbol and
                board[row + 2][col - 2] == symbol and
                board[row + 3][col - 3] == symbol):
                return True  # Diagonal down-left win
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(player, symbol):
    """Prompt player for a move and return the column index."""
    while True:
        try:
            move = input(f"Player {player}, please enter a column: ").upper()
            if not move:
                raise ValueError("Empty input.")
            col = ord(move[0]) - ord('A')
            if not (0 <= col < COLS):
                print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}")
                continue
            return col
        except (ValueError, IndexError):
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}")

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = [i + 1 for i in range(PLAYERS)]
    symbols = PLAYER_SYMBOLS[:PLAYERS]
    
    # Randomly choose starting player
    current_player = random.choice(players)
    current_symbol = symbols[current_player - 1]
    
    print_board(board)
    
    while True:
        col = get_player_move(current_player, current_symbol)
        
        if not is_valid_move(col, board):
            print(f"Column {chr(65 + col)} is full. Try another column.")
            continue
        
        make_move(col, current_symbol, board)
        print_board(board)
        
        if check_win(board, current_symbol):
            print(f"Player {current_player} ({current_symbol}) won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player % PLAYERS) + 1
        current_symbol = symbols[current_player - 1]

if __name__ == "__main__":
    main()
