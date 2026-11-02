import os
import random

# Constants to define the board size and the number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the console screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Check if current player wins
def check_win(board, row, col, checker):
    # Check horizontal, vertical, and two diagonal directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 0
        for offset in range(-3, 4):
            r, c = row + offset * dr, col + offset * dc
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

# Check if the board is full (draw condition)
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(range(NUM_PLAYERS))
    print_board(board)
    
    while True:
        current_checker = CHECKERS[current_player]

        while True:
            try:
                column = input(f"Player {current_checker}, please enter a column: ").strip().upper()
                col_idx = ord(column) - 65
                if col_idx in range(COLUMNS) and board[0][col_idx] == " ":
                    break
                else:
                    print("Invalid column. Try again.")
            except:
                print("Invalid input. Please enter a valid column letter.")

        # Place the checker in the correct row
        for row in range(ROWS-1, -1, -1):
            if board[row][col_idx] == " ":
                board[row][col_idx] = current_checker
                break
                
        print_board(board)

        # Check for win
        if check_win(board, row, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate player turns
        current_player = (current_player + 1) % NUM_PLAYERS

play_game()
