import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
BOARD_FILL = " "

# Create board
def create_board(rows, cols):
    return [[BOARD_FILL for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    col_labels = "  " + "   ".join([chr(65 + i) for i in range(COLS)])
    print(col_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Check for valid column input
def is_valid_column(input_col, board):
    if len(input_col) != 1 or not input_col.isalpha():
        return False
    col = ord(input_col.upper()) - 65
    if not (0 <= col < COLS):
        return False
    if board[0][col] != BOARD_FILL:  # Top cell filled means full column
        return False
    return True

# Place checker in column
def place_checker(player, column, board):
    col = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col] == BOARD_FILL:
            row[col] = CHECKERS[player]
            return

# Check for a win
def check_win(board, player):
    checker = CHECKERS[player]
    
    # Horizontal
    for row in board:
        for c in range(COLS - 3):
            if row[c] == checker and row[c+1] == checker and row[c+2] == checker and row[c+3] == checker:
                return True

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

    return False

# Check for draw
def check_draw(board):
    return all(cell != BOARD_FILL for row in board for cell in row)

# Main function
def play_game():
    # Initialize the board
    board = create_board(ROWS, COLS)
    num_players = 2  # Set to 2 for submission
    players = list(range(num_players))
    random.shuffle(players)
    current_player = players[0]
    
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts!")

    while True:
        # Get player input
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip()
        
        # Validate input
        while not is_valid_column(column, board):
            column = input(f"Invalid input. Player {CHECKERS[current_player]}, enter a valid column: ").strip()
        
        # Place checker
        place_checker(current_player, column, board)
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % num_players

# Run the game
if __name__ == "__main__":
    play_game()
