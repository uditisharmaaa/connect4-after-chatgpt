import os
import random
import string

# Constants for the board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players supported
WIN_LENGTH = 4
COLUMN_LABELS = string.ascii_uppercase[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels
    print(" ", end=" ")
    for c in COLUMN_LABELS:
        print(f" {c}  ", end="")
    print()
    # Print top border
    print("+" + "---+" * len(board[0]))
    # Print rows
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "---+" * len(board[0]))

def choose_starting_player(num_players):
    return random.randint(0, num_players -1)

def is_valid_column(col):
    return col in COLUMN_LABELS

def column_full(board, col_index):
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    # Place checker in lowest open row in column col_index
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1  # Indicates column is full

def check_win(board, row, col, checker):
    # Check directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    # If top row has no empty spots, board is full
    return all(cell != " " for cell in board[0])

def input_column(player_checker):
    while True:
        col = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        if not is_valid_column(col):
            print(f"Invalid column. Please enter a letter from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
            continue
        col_index = COLUMN_LABELS.index(col)
        return col_index

def main():
    board = create_board(ROWS, COLUMNS)
    num_players = PLAYERS
    players = CHECKERS[:num_players]
    current_player_idx = choose_starting_player(num_players)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]
        col_index = input_column(current_checker)
        # Check if column is full before placing
        if column_full(board, col_index):
            print(f"Column {COLUMN_LABELS[col_index]} is full. You lose your turn.")
            # No turn lost on invalid input, but lost if column is full
            current_player_idx = (current_player_idx + 1) % num_players
            print_board(board)
            continue

        row_placed = place_checker(board, col_index, current_checker)
        print_board(board)

        if check_win(board, row_placed, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
