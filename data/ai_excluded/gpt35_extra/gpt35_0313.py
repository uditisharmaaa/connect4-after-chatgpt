import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board

def print_board(board):
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(labels))
    
    # Print board rows
    line = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def is_valid_column(col_char):
    if len(col_char) != 1:
        return False
    col = ord(col_char) - ord('A')
    if col < 0 or col >= COLS:
        return False
    return True

def get_column_index(col_char):
    return ord(col_char) - ord('A')

def place_checker(board, col, checker):
    # Place checker in lowest empty row in column col
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    # Column full
    return -1

def check_four_in_a_row(board, row, col, checker):
    # Directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diagonal down right
        (1,-1)  # diagonal down left
    ]

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = row+dr, col+dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]

    # Randomly choose starting player index
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    
    while True:
        checker = players_checkers[current_player]
        print(f"Player {checker}, please enter a column:")
        user_input = input().strip().upper()

        if not is_valid_column(user_input):
            # invalid input, ask again, same player
            continue
        
        col = get_column_index(user_input)

        row = place_checker(board, col, checker)
        if row == -1:
            # column full, player loses turn
            current_player = (current_player + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        if check_four_in_a_row(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw.")
            break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
