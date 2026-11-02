import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5  # Maximum number of players
CHECKERS = ["X", "O", "V", "H", "M"]  # Player tokens (for max 5 players)
PLAYER_COUNT = 2  # Default player count (can range between 2 and MAX_PLAYERS)
WIN_CONDITION = 4  # Number of checkers in a row needed to win

# Create the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system("clear")  # Clear the terminal
    header = "  " + "   ".join(chr(65 + i) for i in range(COLS))  # Column labels (A, B, C, ...)
    print(header)
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for valid column input
def is_valid_column(input_col, board):
    if len(input_col) != 1 or not input_col.isalpha():
        return False
    col_index = ord(input_col.upper()) - 65
    return 0 <= col_index < COLS and board[0][col_index] == " "

# Drop a checker into the board
def drop_checker(board, col, checker):
    col_index = ord(col.upper()) - 65
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row, col_index

# Check for victory
def check_victory(board, row, col, checker):
    def count_in_direction(delta_row, delta_col):
        count = 0
        r, c = row, col
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += delta_row
            c += delta_col
        return count

    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for delta_row, delta_col in directions:
        if count_in_direction(delta_row, delta_col) + count_in_direction(-delta_row, -delta_col) - 1 >= WIN_CONDITION:
            return True
    return False

# Check for draw
def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    board = create_board()
    players = CHECKERS[:PLAYER_COUNT]
    current_player = random.choice(players)

    print_board(board)
    print(f"Randomly chosen: Player {current_player}")

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_column(user_input, board):
            print("Invalid input! Please enter a valid column.")
            continue

        row, col = drop_checker(board, user_input, current_player)
        print_board(board)

        if check_victory(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch turn
        current_player = players[(players.index(current_player) + 1) % PLAYER_COUNT]

if __name__ == "__main__":
    play_game()
