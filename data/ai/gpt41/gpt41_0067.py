import os
import random
import string

# ----------- CONSTANTS -----------
ROWS = 6          # Number of rows
COLUMNS = 7       # Number of columns (max 26)
NUM_PLAYERS = 2   # Supported: 2 - 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players
WIN_LENGTH = 4    # Number of checkers in line to win

# ----------- BOARD INITIALIZATION -----------

def create_board(rows, cols):
    # Create a ROWS x COLUMNS 2D list filled with whitespaces
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # For Unix/Linux/Mac. For Windows, use 'cls'
    cols = len(board[0])
    # Header A, B, ... (up to max columns)
    col_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(col_labels)
    print('+' + '---+'*cols)
    for row in board:
        # Build row contents
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+'*cols)

# ----------- PLAYER TURN AND INPUT -----------

def get_player_input(player_checker, board):
    cols = len(board[0])
    valid_cols = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in valid_cols:
            print(f"Invalid input! Please enter one of {', '.join(valid_cols)}.")
            continue
        col_index = valid_cols.index(user_input)
        # Check if column is full
        if board[0][col_index] != ' ':
            print("This column is full! You lose your turn.")
            return None  # Lose the turn
        return col_index

def place_checker(board, col, checker):
    rows = len(board)
    # Start from bottom row, find first available spot
    for row in reversed(range(rows)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Shouldn't happen, handled in input

# ----------- WIN AND DRAW CHECKING -----------

def check_win(board, last_row, last_col, checker):
    # Check all directions: horizontal, vertical, diag1( \ ), diag2 ( / )
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Count the last placed checker
        # Check in + direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in - direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    # If first row (top) contains any space, not draw
    return all(cell != ' ' for cell in board[0])

# ----------- MAIN GAME LOOP -----------

def main():
    # Set up board and player info
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    # Random start
    current_player = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    print(f"Randomly selected Player {players[current_player]} starts!\n")
    game_over = False

    while not game_over:
        player_checker = players[current_player]
        col_index = get_player_input(player_checker, board)
        if col_index is None:
            # Turn lost if column full
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        # Place checker
        row, col = place_checker(board, col_index, player_checker)
        print_board(board)
        # Check win/draw
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
