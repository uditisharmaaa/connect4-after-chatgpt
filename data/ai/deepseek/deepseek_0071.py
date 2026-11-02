import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    """Initialize the game board with empty spaces."""
    board = []
    for _ in range(BOARD_ROWS):
        row = [' '] * BOARD_COLS
        board.append(row)
    return board

def print_board(board):
    """Print the game board with labels and borders."""
    # Print column labels
    header = '   '
    for col in range(BOARD_COLS):
        header += f" {chr(65 + col)}   "
    print(header)
    
    # Print top border
    border = '+' + ('---+' * BOARD_COLS)
    print(border)
    
    # Print each row with borders
    for row in range(BOARD_ROWS):
        row_str = '|'
        for col in range(BOARD_COLS):
            row_str += f" {board[row][col]} |"
        print(row_str)
        print(border)

def is_valid_move(board, column):
    """Check if the move is valid (column exists and has space)."""
    if column < 0 or column >= BOARD_COLS:
        return False
    return board[0][column] == ' '

def make_move(board, column, player_char):
    """Place the player's checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_char
            return True
    return False

def check_winner(board, player_char):
    """Check if the player has 4 in a row (horizontally, vertically, or diagonally)."""
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player_char and 
                board[row][col+1] == player_char and 
                board[row][col+2] == player_char and 
                board[row][col+3] == player_char):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == player_char and 
                board[row+1][col] == player_char and 
                board[row+2][col] == player_char and 
                board[row+3][col] == player_char):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == player_char and 
                board[row+1][col+1] == player_char and 
                board[row+2][col+2] == player_char and 
                board[row+3][col+3] == player_char):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if (board[row][col] == player_char and 
                board[row+1][col-1] == player_char and 
                board[row+2][col-2] == player_char and 
                board[row+3][col-3] == player_char):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def get_column_input(player_char):
    """Get player input for column selection."""
    while True:
        col_input = input(f"Player {player_char}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        column = ord(col_input) - ord('A')
        if column < 0 or column >= BOARD_COLS:
            print(f"Column must be between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        return column

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = PLAYER_CHARS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    
    while not game_over:
        clear_screen()
        print_board(board)
        
        player_char = players[current_player_idx]
        column = get_column_input(player_char)
        
        if not is_valid_move(board, column):
            print("Column is full. Turn lost.")
            input("Press Enter to continue...")
        else:
            make_move(board, column, player_char)
            if check_winner(board, player_char):
                clear_screen()
                print_board(board)
                print(f"Player {player_char} won!")
                game_over = True
            elif is_board_full(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                game_over = True
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
