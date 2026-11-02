import os
import random

# Constants
ROWS, COLS = 6, 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# Initialize board
def init_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

# Print board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check win conditions
def check_win(board, player, r, c):
    def check_direction(dr, dc):
        count = 0
        for i in range(-3, 4):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
    
    return (check_direction(1, 0) or  # Vertical
            check_direction(0, 1) or  # Horizontal
            check_direction(1, 1) or  # Diagonal \
            check_direction(1, -1))   # Diagonal /

# Check for draw
def check_draw(board):
    return all(board[0][c] != EMPTY_CELL for c in range(COLS))

# Place checker
def place_checker(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            board[r][col] = player
            return r
    return -1

# Get valid input
def get_valid_input():
    while True:
        col = input("Please enter a column: ").strip().upper()
        if len(col) == 1 and col.isalpha():
            col_idx = ord(col) - 65
            if 0 <= col_idx < COLS:
                return col_idx
        print("Invalid input. Try again.")

# Main function
def connect_4():
    # Initialize game
    board = init_board(ROWS, COLS)
    num_players = 2
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    print_board(board)
    print(f"Player {current_player} starts!")

    # Game loop
    while True:
        print(f"Player {current_player}, it's your turn.")
        col = get_valid_input()

        # Place checker
        row = place_checker(board, col, current_player)
        if row == -1:
            print("Column full. Try another.")
            continue

        print_board(board)

        # Check for win or draw
        if check_win(board, current_player, row, col):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # Switch player
        current_player = players[(players.index(current_player) + 1) % num_players]

# Run game
if __name__ == "__main__":
    connect_4()
