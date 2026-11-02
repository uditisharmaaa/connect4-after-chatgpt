import os
import random
import string

# Constants for board size and players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    
    horizontal_line = "+" + "---+" * len(board[0])
    for row in board:
        print(horizontal_line)
        print("| " + " | ".join(row) + " |")
    print(horizontal_line)

def input_column(player_checker, columns):
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if col_input not in string.ascii_uppercase[:columns]:
            print("Invalid column letter. Please enter a valid column.")
            continue
        return string.ascii_uppercase.index(col_input)

def place_checker(board, col, checker):
    # Iterate from bottom row upwards to find empty spot
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full -> return None to signal losing turn
    return None

def check_winner(board, row, col, checker):
    # Check all four directions: horizontal, vertical, and two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = PLAYERS_CHECKERS[current_player_idx]
        col = input_column(checker, COLUMNS)
        placed_row = place_checker(board, col, checker)
        if placed_row is None:
            # Column full, player loses turn
            print(f"Column {string.ascii_uppercase[col]} is full. You lose your turn.")
            # still print board after warning
            print_board(board)
            # switch player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue
        
        print_board(board)

        # Check win condition
        if check_winner(board, placed_row, col, checker):
            print(f"Player {checker} won!")
            break
        
        # Check draw condition
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
