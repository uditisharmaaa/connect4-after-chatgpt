import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Can be from 2 to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players in order

# Initialize the board
def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    # Clear the screen
    os.system('clear')  # Use 'cls' for Windows
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---+' * COLS)

# Check if a column is valid (within bounds and not full)
def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

# Drop a checker into a column
def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

# Check if a player has won
def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row - 1][col + 1] == checker and 
                board[row - 2][col + 2] == checker and 
                board[row - 3][col + 3] == checker):
                return True
    return False

# Check if the board is full (draw)
def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game function
def play_game():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        
        # Get valid input
        while True:
            try:
                col_input = input().upper()
                if len(col_input) != 1 or not col_input.isalpha():
                    raise ValueError
                col = ord(col_input) - ord('A')
                if not is_valid_column(board, col):
                    raise ValueError
                break
            except ValueError:
                print(f"Invalid input. Player {checker}, please enter a valid column (A-{chr(ord('A') + COLS - 1)}):")
        
        # Drop the checker
        drop_checker(board, col, checker)
        
        # Check for win
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    play_game()
