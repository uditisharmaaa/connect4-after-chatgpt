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
    os.system('clear')  # or 'cls' for Windows
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---+" + "---+" * (COLS - 1))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+" + "---+" * (COLS - 1))

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                if c <= COLS - 4 and all(board[r][c + i] == player for i in range(4)):
                    return True
                if r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4)):
                    return True
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == player for i in range(4)):
                    return True
    return False

# Check for draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    turn_count = 0

    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column (A-G):")
        col_input = input().strip().upper()

        if len(col_input) != 1 or ord(col_input) < 65 or ord(col_input) >= 65 + COLS:
            print("Invalid input. Try again.")
            continue

        col = ord(col_input) - 65
        for row in reversed(board):
            if row[col] == " ":
                row[col] = current_player
                break
        else:
            print("Column is full! Try again.")
            continue

        turn_count += 1

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = PLAYERS[turn_count % len(PLAYERS)]

if __name__ == "__main__":
    main()
