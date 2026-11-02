import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
WINNING_LENGTH = 4

# Initialize the game board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the game board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + col) for col in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Check if a move is valid
def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == ' '

# Place a checker in the board
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

# Check for a win
def check_win(board, checker):
    # Check horizontal, vertical and diagonal connections
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == checker:
                # Check horizontal
                if col + WINNING_LENGTH <= COLS and all(board[row][col + i] == checker for i in range(WINNING_LENGTH)):
                    return True
                # Check vertical
                if row + WINNING_LENGTH <= ROWS and all(board[row + i][col] == checker for i in range(WINNING_LENGTH)):
                    return True
                # Check diagonal (down-right)
                if row + WINNING_LENGTH <= ROWS and col + WINNING_LENGTH <= COLS and all(board[row + i][col + i] == checker for i in range(WINNING_LENGTH)):
                    return True
                # Check diagonal (down-left)
                if row + WINNING_LENGTH <= ROWS and col - WINNING_LENGTH + 1 >= 0 and all(board[row + i][col - i] == checker for i in range(WINNING_LENGTH)):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Create and initialize the board
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:2]  # Set to 2 players
    current_player = random.choice(players)
    turns = 0

    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        if len(col_input) != 1 or col_input < 'A' or col_input > 'G':
            print("Invalid input. Please enter a letter from A to G.")
            continue

        col = ord(col_input) - 65  # Convert letter to column index
        if not is_valid_move(board, col):
            print("Column is full. Please try another column.")
            continue

        place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        turns += 1
        current_player = players[turns % len(players)]  # Switch to the next player

if __name__ == "__main__":
    main()
