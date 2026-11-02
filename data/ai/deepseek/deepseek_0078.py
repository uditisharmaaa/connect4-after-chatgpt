import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create an empty game board."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the game board with labeled columns."""
    # Print column letters
    print('  ' + '   '.join([chr(65 + i) for i in range(NUM_COLS)]))
    
    # Print the board rows
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+---' * NUM_COLS + '+')

def get_valid_move(board, player):
    """Prompt the player for a valid move and return the column index."""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter from A to " + chr(65 + NUM_COLS - 1))
            continue
        
        col = ord(move) - ord('A')
        if col < 0 or col >= NUM_COLS:
            print("Column out of bounds. Please choose between A and " + chr(65 + NUM_COLS - 1))
            continue
        
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, player):
    """Place the player's checker in the specified column at the lowest available row."""
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """Check if the player has won by getting 4 in a row horizontally, vertically, or diagonally."""
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    
    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    
    # Check diagonal down-right
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    
    # Check diagonal down-left
    for row in range(NUM_ROWS - 3):
        for col in range(3, NUM_COLS):
            if (board[row][col] == player and 
                board[row+1][col-1] == player and 
                board[row+2][col-2] == player and 
                board[row+3][col-3] == player):
                return True
    
    return False

def is_draw(board):
    """Check if the game is a draw by verifying if the board is full."""
    return all(cell != ' ' for cell in board[0])

def main():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        col = get_valid_move(board, current_player)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
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
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
