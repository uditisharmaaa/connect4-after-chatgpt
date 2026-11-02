import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

def initialize_board():
    """Initialize an empty board with ROWS rows and COLS columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column letters
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print top border
    print('+' + ('---+' * COLS))
    
    # Print each row
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + ('---+' * COLS))

def get_player_checkers(num_players):
    """Return a list of player checkers based on num_players."""
    checkers = ['X', 'O', 'V', 'H', 'M']
    return checkers[:num_players]

def is_valid_column(col, board):
    """Check if the column is valid and not full."""
    if len(col) != 1:
        return False
    col_idx = ord(col.upper()) - ord('A')
    return 0 <= col_idx < COLS and board[0][col_idx] == ' '

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the column."""
    col_idx = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = get_player_checkers(NUM_PLAYERS)
    current_player = random.choice(players)
    
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}, please enter a column: ")
        col = input().strip().upper()
        
        if not is_valid_column(col, board):
            print("Invalid column. Try again.")
            continue
        
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
            
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
