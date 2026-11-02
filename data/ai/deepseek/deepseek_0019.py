import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    # Print column letters
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        col = ord(col_input) - ord('A')
        if col < 0 or col >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col] != ' ':
            print("This column is full. Please choose another.")
            continue
        return col

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Search in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Search in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(board[0][col] != ' ' for col in range(COLS))

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    """Main game loop."""
    global current_player
    board = initialize_board()
    current_player = random.choice(CHECKERS)
    clear_screen()
    print(f"Player {current_player} starts the game.")
    print_board(board)

    while True:
        col = get_valid_column(board)
        row = place_checker(board, col, current_player)
        clear_screen()
        print_board(board)

        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("Game over. It's a draw!")
            break

        # Switch to the next player
        current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
