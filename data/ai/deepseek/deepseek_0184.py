import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2

PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create and initialize a new board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column labels
    print("  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0]))))
    
    # Print top border
    print("+" + "---+" * len(board[0]))
    
    # Print each row
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, cols):
    """Check if the column input is valid."""
    if len(column) != 1:
        return False
    col_char = column.upper()
    return 'A' <= col_char <= chr(ord('A') + cols - 1)

def get_player_move(board, player_token):
    """Get and validate player move."""
    while True:
        col = input(f"Player {player_token}, please enter a column: ").strip().upper()
        if is_valid_column(col, len(board[0])):
            col_idx = ord(col) - ord('A')
            if board[0][col_idx] == " ":  # Check if column is not full
                return col_idx
            print("Column is full! Choose another column.")
        else:
            print("Invalid column! Please enter a valid column letter.")

def drop_checker(board, col_idx, player_token):
    """Place the checker in the specified column at the lowest available row."""
    for row_idx in range(len(board) - 1, -1, -1):
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_token
            return row_idx
    return -1  # Shouldn't happen if column is checked for validity before

def check_win(board, row, col, player_token):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # horizontal
        (1, 0),    # vertical
        (1, 1),    # diagonal down-right
        (1, -1)    # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # the current cell
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_token:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == player_token:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != " " for row in board for cell in row)

def main():
    """Main game loop."""
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = PLAYER_TOKENS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        os.system('clear')
        print_board(board)
        
        current_player = players[current_player_idx]
        col_idx = get_player_move(board, current_player)
        row_idx = drop_checker(board, col_idx, current_player)
        
        if check_win(board, row_idx, col_idx, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
