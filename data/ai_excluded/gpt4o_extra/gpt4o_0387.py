import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    """Initialize the game board to be empty."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_input(column, board):
    """Check if the provided column input is valid."""
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    if col_index < 0 or col_index >= COLUMNS:
        return False
    return board[0][col_index] == ' '

def place_checker(board, column, checker):
    """Place the checker in the chosen column."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return

def check_winner(board, checker):
    """Check if the current checker has any winning condition."""
    # Check horizontal, vertical, diagonal /
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                col <= COLUMNS - 4 and
                all(board[row][col + i] == checker for i in range(4))
            ):
                return True
            if (
                row <= ROWS - 4 and
                all(board[row + i][col] == checker for i in range(4))
            ):
                return True
            if (
                col <= COLUMNS - 4 and row <= ROWS - 4 and
                all(board[row + i][col + i] == checker for i in range(4))
            ):
                return True
            if (
                col >= 3 and row <= ROWS - 4 and
                all(board[row + i][col - i] == checker for i in range(4))
            ):
                return True
    return False

def check_draw(board):
    """Check if the board is completely filled and results in a draw."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Function to manage the overall game logic."""
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip()

        # Validate user input
        if not is_valid_input(column, board):
            print("Invalid input. Please try again.")
            continue
        
        # Place the checker
        place_checker(board, column, CHECKERS[current_player])
        
        # Check for win or draw
        if check_winner(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
            
        # Switch players
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
