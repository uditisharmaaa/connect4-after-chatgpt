import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = 2  # Set to 2 for submission as requested
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(labels))
    # Print the board rows
    for row in board:
        print("+" + "---+" * len(row))
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * len(board[0]))

def get_valid_column(player, board):
    cols = len(board[0])
    while True:
        col = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not ('A' <= col <= chr(ord('A') + cols -1)):
            print("Invalid column. Please enter a letter corresponding to the columns.")
            continue
        col_idx = ord(col) - ord('A')
        # Check if column is full
        if board[0][col_idx] != ' ':
            # Turn lost if full column
            return -1
        return col_idx

def place_checker(board, col, checker):
    # Place checker in lowest empty row in col
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    # Should not get here if checked for full column before
    return None

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # Check diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # Check diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def check_draw(board):
    # Draw if no empty spot at top row
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col = get_valid_column(current_checker, board)
        if col == -1:
            # Column full, turn lost
            print(f"Column is full. Player {current_checker} loses the turn.")
            current_player_idx = (current_player_idx +1) % PLAYERS
            continue
        place_checker(board, col, current_checker)
        print_board(board)
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current_player_idx = (current_player_idx +1) % PLAYERS

if __name__ == "__main__":
    main()
