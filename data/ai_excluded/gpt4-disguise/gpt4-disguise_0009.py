import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
LETTERS = [chr(i) for i in range(65, 91)]  # A-Z

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(LETTERS[:COLS]))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for win
def check_win(board, player):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True
                
    # Vertical check
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

    return False

# Check for draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Place checker in column
def drop_checker(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player
            return True
    return False

# Input validation
def get_valid_column(board):
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) != 1 or col not in LETTERS[:COLS]:
            print("Invalid column. Try again.")
            continue
        col_index = LETTERS.index(col)
        if board[0][col_index] != " ":
            print("Column is full. Pick another one.")
            continue
        return col_index

# Main game
def play_game():
    board = create_board()
    active_players = CHECKERS[:PLAYERS]
    current_player = random.choice(active_players)

    print_board(board)
    print(f"Player {current_player} starts!")

    while True:
        print_board(board)
        print(f"Player {current_player}, it's your turn.")
        column = get_valid_column(board)
        drop_checker(board, column, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        index = active_players.index(current_player)
        current_player = active_players[(index + 1) % PLAYERS]

# Start the game
play_game()
