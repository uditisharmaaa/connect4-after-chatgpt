import random
import os
import sys

# ========== CONSTANTS ==========
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

LETTERS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]

# ========== FUNCTIONS ==========

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Creates a 2D board with spaces ' '."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board, with column labels."""
    header = "  " + "   ".join(LETTERS)
    print(header)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_next_open_row(board, col):
    """Returns the lowest empty row index in the column, or None if column is full."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def valid_column(col_str):
    """Checks if col_str is a valid single letter for column."""
    return len(col_str) == 1 and col_str in LETTERS

def check_for_win(board, checker):
    """Checks if there are 4 in a row of checker."""
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal \ check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    # Diagonal / check
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def board_full(board):
    """Checks if the board is full."""
    for row in board:
        if ' ' in row:
            return False
    return True

# ========== MAIN GAME ==========
def main():
    random.seed()
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    player_names = ["Player " + players[i] for i in range(NUM_PLAYERS)]
    
    current_player = random.randint(0, NUM_PLAYERS-1)

    while True:
        clear_screen()
        print_board(board)
        print()
        print("{} ({}), please enter a column:".format(player_names[current_player], players[current_player]))
        col_input = input(">> ").strip().upper()
        
        # Input validation
        while True:
            if not valid_column(col_input):
                print("Invalid input. Try again.")
            else:
                col = LETTERS.index(col_input)
                row = get_next_open_row(board, col)
                if row is None:
                    print("Column is full. You lose your turn!")
                    current_player = (current_player + 1) % NUM_PLAYERS
                    input("Press Enter to continue...")
                    break
                else:
                    # Place checker
                    board[row][col] = players[current_player]
                    # Check for win
                    if check_for_win(board, players[current_player]):
                        clear_screen()
                        print_board(board)
                        print()
                        print("{} won!".format(player_names[current_player]))
                        sys.exit(0)
                    # Check for draw
                    elif board_full(board):
                        clear_screen()
                        print_board(board)
                        print()
                        print("Game is a draw!")
                        sys.exit(0)
                    # Continue game
                    current_player = (current_player + 1) % NUM_PLAYERS
                    break
            print()
            print("Please enter a valid column:")
            col_input = input(">> ").strip().upper()

if __name__ == '__main__':
    main()
