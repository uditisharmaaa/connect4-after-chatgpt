import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers (A, B, C, ...)
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the top border
    top_border = '+' + ('---+' * COLS)
    print(top_border)
    
    # Print each row
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print(top_border)

def get_valid_column(current_player, board):
    """Get a valid column input from the player."""
    valid_columns = [chr(65 + i) for i in range(COLS)]
    while True:
        try:
            col = input(f"Player {current_player}, please enter a column: ").upper()
            if col not in valid_columns:
                print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
                continue
            
            col_index = ord(col) - ord('A')
            if board[0][col_index] != ' ':
                print("Column is full. Please choose another column.")
                continue
                
            return col_index
        except EOFError:
            print("\nExiting game.")
            exit()
        except:
            print("Invalid input. Please try again.")

def drop_checker(board, col, checker):
    """Drop the checker into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Column is full

def check_win(board, row, col):
    """Check if the last move caused a win."""
    checker = board[row][col]
    
    # Check horizontal
    for c in range(col - 3, col + 1):
        if c >= 0 and c + 3 < COLS:
            if board[row][c] == board[row][c+1] == board[row][c+2] == board[row][c+3] == checker:
                return True
    
    # Check vertical
    for r in range(row - 3, row + 1):
        if r >= 0 and r + 3 < ROWS:
            if board[r][col] == board[r+1][col] == board[r+2][col] == board[r+3][col] == checker:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for r, c in zip(range(row - 3, row + 1), range(col - 3, col + 1)):
        if r >= 0 and r + 3 < ROWS and c >= 0 and c + 3 < COLS:
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == checker:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for r, c in zip(range(row + 3, row - 1, -1), range(col - 3, col + 1)):
        if r - 3 >= 0 and r < ROWS and c >= 0 and c + 3 < COLS:
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == checker:
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"Player {PLAYERS[current_player]} starts first!")
    print_board(board)
    
    while True:
        checker = PLAYERS[current_player]
        col = get_valid_column(checker, board)
        row = drop_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, row, col):
            print(f"Player {checker} won!")
            break
        
        if check_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
