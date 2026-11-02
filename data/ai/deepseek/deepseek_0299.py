import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players


def initialize_board():
    """Initialize an empty game board with given dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the game board with column labels."""
    # Clear the screen before printing
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print(border)


def get_valid_column(board):
    """Prompt the player for a column input and validate it."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not col_input:
            print("Please enter a column letter.")
            continue
        
        col = ord(col_input[0]) - ord('A')
        if 0 <= col < COLS:
            if board[0][col] == ' ':  # Check if the top cell is empty (column not full)
                return col
            else:
                print("That column is full. Choose another.")
        else:
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")


def drop_piece(board, col, player):
    """Drop a piece into the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1  # Column is full (should not happen if validated)


def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False


def is_draw(board):
    """Check if the game is a draw (board full)."""
    return all(cell != ' ' for cell in board[0])


def main():
    global current_player
    board = initialize_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        row = drop_piece(board, col, current_player)
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]


if __name__ == "__main__":
    main()
