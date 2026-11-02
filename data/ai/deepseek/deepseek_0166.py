import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty board with given dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print board rows
    for row in board:
        print('+' + '---+' * BOARD_COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+' + '---+' * BOARD_COLS)

def is_valid_column(column):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return 'A' <= col_char <= chr(65 + BOARD_COLS - 1)

def place_checker(board, column, player):
    """
    Place the player's checker in the specified column.
    Returns the row where the checker was placed, or -1 if column is full.
    """
    col_index = ord(column.upper()) - 65
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        # Check for draw
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Get player input
        while True:
            column = input(f"Player {current_player}, please enter a column: ").strip()
            if is_valid_column(column):
                break
            print("Invalid input. Please enter a valid column letter.")
        
        # Place checker
        column_upper = column.upper()
        row = place_checker(board, column_upper, current_player)
        if row == -1:
            print(f"Column {column_upper} is full. Player {current_player} loses turn.")
        else:
            # Check for win
            if check_win(board, row, ord(column_upper) - 65, current_player):
                os.system('clear')
                print_board(board)
                print(f"Player {current_player} won!")
                break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
