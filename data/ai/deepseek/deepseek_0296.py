import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    header = "  " + "   ".join([chr(65 + i) for i in range(COLS)]) + "  "
    print(header)
    
    # Print board rows with borders
    for row in board:
        row_str = "| " + " | ".join(row) + " |"
        border = "+" + ("---+") * COLS
        print(border)
        print(row_str)
    print(border)

def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    return 0 <= col < COLS and board[0][col] == " "

def make_move(board, col, player):
    """Place a player's checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return (row, col)
    return None

def check_win(board, row, col, player):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    clear_screen()
    print(f"Player {current_player} starts first!\n")
    print_board(board)
    
    while True:
        try:
            col_input = input(f"Player {current_player}, please enter a column: ").upper()
            if not col_input or len(col_input) != 1:
                raise ValueError("Invalid input. Enter a single letter.")
            col = ord(col_input) - ord('A')
            if not is_valid_move(board, col):
                raise ValueError("Invalid move. Column is full or out of bounds.")
            break
        except ValueError as e:
            print(e)
    
    move = make_move(board, col, current_player)
    clear_screen()
    print_board(board)
    
    if check_win(board, move[0], move[1], current_player):
        print(f"Player {current_player} won!")
        return
    
    if is_draw(board):
        print("Game ended in a draw!")
        return
    
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
    while True:
        try:
            col_input = input(f"Player {current_player}, please enter a column: ").upper()
            if not col_input or len(col_input) != 1:
                raise ValueError("Invalid input. Enter a single letter.")
            col = ord(col_input) - ord('A')
            if not is_valid_move(board, col):
                raise ValueError("Invalid move. Column is full or out of bounds.")
            break
        except ValueError as e:
            print(e)
    
    move = make_move(board, col, current_player)
    clear_screen()
    print_board(board)
    
    if check_win(board, move[0], move[1], current_player):
        print(f"Player {current_player} won!")
        return
    
    if is_draw(board):
        print("Game ended in a draw!")
        return
    
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
