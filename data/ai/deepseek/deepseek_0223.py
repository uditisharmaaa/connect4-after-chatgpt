import os
import random

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

# Player symbols in order
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board in the specified format."""
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print board rows
    for row in board:
        border = '+'.join(['---'] * BOARD_COLS)
        print(f'+{border}+')
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    
    # Print bottom border
    print(f'+{"+".join(["---"] * BOARD_COLS)}+')

def get_valid_input(current_player):
    """Get and validate player input for column selection."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= BOARD_COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + BOARD_COLS - 1)}.")
            continue
        return col_index

def place_checker(board, col_index, player_symbol):
    """Place the checker in the specified column at the lowest available row."""
    for row_index in range(BOARD_ROWS - 1, -1, -1):
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = player_symbol
            return True
    return False  # Column is full

def check_win(board, player_symbol):
    """Check if the current player has won the game."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player_symbol and
                board[row][col+1] == player_symbol and
                board[row][col+2] == player_symbol and
                board[row][col+3] == player_symbol):
                return True

    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == player_symbol and
                board[row+1][col] == player_symbol and
                board[row+2][col] == player_symbol and
                board[row+3][col] == player_symbol):
                return True

    # Check diagonal (down-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player_symbol and
                board[row+1][col+1] == player_symbol and
                board[row+2][col+2] == player_symbol and
                board[row+3][col+3] == player_symbol):
                return True

    # Check diagonal (down-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if (board[row][col] == player_symbol and
                board[row+1][col-1] == player_symbol and
                board[row+2][col-2] == player_symbol and
                board[row+3][col-3] == player_symbol):
                return True

    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            return False
    return True

def main():
    """Main game loop."""
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player = PLAYER_SYMBOLS[current_player_index]
    
    while True:
        os.system('clear')
        print_board(board)
        
        col_index = get_valid_input(current_player)
        if not place_checker(board, col_index, current_player):
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_player} loses their turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, current_player):
                os.system('clear')
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_board_full(board):
                os.system('clear')
                print_board(board)
                print("The game is a draw!")
                break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_player = PLAYER_SYMBOLS[current_player_index]

if __name__ == "__main__":
    main()
