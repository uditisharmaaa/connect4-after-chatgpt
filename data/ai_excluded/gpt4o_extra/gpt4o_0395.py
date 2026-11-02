import random
import os

# Constants defining board dimensions and number of players.
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checker symbols for players.
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a game board with given dimensions initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current game board."""
    os.system('clear')
    # Print column headers
    headers = "  ".join(chr(i + ord('A')) for i in range(len(board[0])))
    print(headers)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def get_valid_input(board):
    """Prompt the player for a valid column input."""
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if col_input.isalpha() and len(col_input) == 1:
            col_index = ord(col_input) - ord('A')
            if 0 <= col_index < len(board[0]) and board[0][col_index] == " ":
                return col_index
        print("Invalid input. Please enter a valid column letter.")

def place_checker(board, col, checker):
    """Place checker in the specified column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            break

def check_win(board, checker):
    """Check if the current player has won."""
    def check_line(r, c, dr, dc):
        for i in range(4):
            if not (0 <= r < NUM_ROWS and 0 <= c < NUM_COLS):
                return False
            if board[r][c] != checker:
                return False
            r += dr
            c += dc
        return True
    
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if check_line(row, col, 0, 1) or check_line(row, col, 1, 0) or check_line(row, col, 1, 1) or check_line(row, col, 1, -1):
                return True
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize board and player settings
    board = create_board(NUM_ROWS, NUM_COLS)
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(player_checkers)
    
    print_board(board)
    while True:
        print(f"Player {current_player}, ", end="")
        col = get_valid_input(board)
        place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        current_player = player_checkers[(player_checkers.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
