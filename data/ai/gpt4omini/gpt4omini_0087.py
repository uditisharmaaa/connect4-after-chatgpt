import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLS)))  # Column labels A to G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check for a win
def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Get the next available row for a column
def get_next_available_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

# Main game loop
def play_game():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if col_input not in chr(i) for i in range(65, 65 + COLS):
            print("Invalid input. Please enter a letter from A to G.")
            continue
            
        col = ord(col_input) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please enter a letter from A to G.")
            continue

        row = get_next_available_row(board, col)
        
        if row is not None:
            board[row][col] = current_player
            print_board(board)
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break

            # Switch player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Column is full. Please choose another column.")

if __name__ == "__main__":
    play_game()
