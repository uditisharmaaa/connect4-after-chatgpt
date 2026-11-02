import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board with the specified dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print the board rows with separators
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def is_valid_column(column):
    """Check if the input column is valid."""
    if len(column) != 1:
        return False
    char = column.upper()
    return 'A' <= char <= chr(65 + COLS - 1)

def place_checker(board, column, checker):
    """
    Place the checker in the specified column.
    Returns the row where the checker was placed or -1 if the column is full.
    """
    col_idx = ord(column.upper()) - 65
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        # Check in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    
    while True:
        os.system('clear')
        print_board(board)
        
        player_input = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not is_valid_column(player_input):
            print("Invalid input. Please enter a valid column (A-" + chr(65 + COLS - 1) + ").")
            input("Press Enter to continue...")
            continue
        
        col = player_input.upper()
        row = place_checker(board, col, current_player)
        
        if row == -1:
            print("Column is full. You lose your turn.")
            input("Press Enter to continue...")
        else:
            if check_win(board, row, ord(col) - 65, current_player):
                os.system('clear')
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if is_draw(board):
                os.system('clear')
                print_board(board)
                print("Game ended in a draw!")
                break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
