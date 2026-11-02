import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Default to 2 players
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Only take needed players

def create_board():
    """Create and return an empty board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with column labels and borders."""
    # Print column labels
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print top border
    print('+' + ('---+' * COLS))
    for row in board:
        # Print row with content and borders
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row border
        print('+' + ('---+' * COLS))

def get_valid_move(board, player):
    """
    Get a valid column letter from the player.
    Keep asking until a valid input is provided.
    """
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) != 1:
            print("Please enter a single letter.")
            continue
        col = ord(move) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col] != ' ':
            print("That column is full. Choose another.")
            continue
        return col

def place_checker(board, col, player):
    """
    Place the player's checker in the specified column.
    The checker falls to the lowest available row.
    """
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def check_win(board, player):
    """
    Check if the player has won by having 4 consecutive checkers
    horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row-1][col+1] == player and 
                board[row-2][col+2] == player and 
                board[row-3][col+3] == player):
                return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    
    while not game_over:
        os.system('clear')
        print_board(board)
        current_player = PLAYERS[current_player_idx]
        col = get_valid_move(board, current_player)
        place_checker(board, col, current_player)
        
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            game_over = True
        elif is_board_full(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
