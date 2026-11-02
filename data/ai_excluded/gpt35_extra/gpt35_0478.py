import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2  # Change to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column letters
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print(" ", end=" ")
    for letter in letters:
        print(f" {letter}  ", end="")
    print()
    # Print board with row borders
    for row in board:
        print("+" + "---+" * len(row))
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * len(board[0]))

def get_player_input(player_checker, board):
    cols = len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            # Invalid length
            continue
        if col_input not in letters:
            # Not a valid column letter
            continue
        col = ord(col_input) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # According to assignment: player loses turn if column full
            return None
        return col

def place_checker(board, col, checker):
    # Place checker on the lowest empty spot in the column
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Should never get here if called correctly (col full handled earlier)
    return None, None

def check_winner(board, last_row, last_col, checker):
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    # If top row has no empty space, board is full
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players_checkers = CHECKERS[:PLAYERS]

    # Choose random starting player
    current_player_idx = random.randint(0, PLAYERS - 1)

    print_board(board)
    while True:
        checker = players_checkers[current_player_idx]
        col = get_player_input(checker, board)
        if col is None:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue
        row, col_check = place_checker(board, col, checker)
        print_board(board)
        # Check for win
        if check_winner(board, row, col_check, checker):
            print(f"Player {checker} won!")
            break
        # Check for draw
        if check_draw(board):
            print("Game is a draw!")
            break
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
