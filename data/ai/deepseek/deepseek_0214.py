import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Print column letters
    columns = '    ' + '   '.join(chr(65 + i) for i in range(COLS))
    print(columns)
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---+' * COLS)

def is_valid_move(board, col):
    """Check if the column is a valid move."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def drop_checker(board, col, symbol):
    """Drop the checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return True
    return False

def check_winner(board, symbol):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row][col+1] == symbol and 
                board[row][col+2] == symbol and 
                board[row][col+3] == symbol):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == symbol and 
                board[row+1][col] == symbol and 
                board[row+2][col] == symbol and 
                board[row+3][col] == symbol):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == symbol and 
                board[row+1][col+1] == symbol and 
                board[row+2][col+2] == symbol and 
                board[row+3][col+3] == symbol):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == symbol and 
                board[row+1][col-1] == symbol and 
                board[row+2][col-2] == symbol and 
                board[row+3][col-3] == symbol):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full."""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) == 1 and 'A' <= column <= chr(65 + COLS - 1):
            return ord(column) - ord('A')
        print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}")

def main():
    """Main function to run the Connect 4 game."""
    global current_player
    board = initialize_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    clear_screen()
    print_board(board)
    
    while True:
        col = get_valid_column()
        
        if not is_valid_move(board, col):
            print("Column is full. Try another column.")
            continue
        
        drop_checker(board, col, current_player)
        clear_screen()
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("Game is a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
