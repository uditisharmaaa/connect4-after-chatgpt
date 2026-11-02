import os
import random

# Constants for the game dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the terminal screen
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1

def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == " "

def check_winner(board, player):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True

    # Check vertical locations for win
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if len(col_input) != 1 or col_input < 'A' or col_input > chr(65 + COLS - 1):
            print("Invalid input. Please enter a letter between A and G.")
            continue
        
        col = ord(col_input) - 65

        if not is_valid_move(board, col):
            print("Column is full. Choose another column.")
            continue

        row = get_next_open_row(board, col)
        board[row][col] = current_player
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(current_index + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
