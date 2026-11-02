import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board with lines
    line = "+---" * COLUMNS + "+"
    for row in range(ROWS):
        print(line)
        row_str = "|"
        for col in range(COLUMNS):
            row_str += " {} |".format(board[row][col])
        print(row_str)
    print(line)

def get_valid_column_input(board, player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in COLUMN_LABELS:
            # Invalid input: not a single character or not in column labels
            continue
        col = ord(inp) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn
            print(f"Column {inp} is full. You lose your turn.")
            return None
        return col

def place_checker(board, col, player_checker):
    # Place checker in lowest available spot in column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return row, col  # Return position where checker placed
    return None  # Should not happen as we check full before

def check_winner(board, row, col, player_checker):
    # Directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count current checker
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    for c in range(COLUMNS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    player_order = list(range(PLAYERS))
    # Randomly select starting player
    current_player_index = random.choice(player_order)
    print_board(board)

    while True:
        current_checker = CHECKERS[player_order[current_player_index]]
        col = get_valid_column_input(board, current_checker)
        if col is None:
            # Player loses turn, move to next player
            current_player_index = (current_player_index + 1) % PLAYERS
            continue
        row, col_placed = place_checker(board, col, current_checker)
        print_board(board)
        if check_winner(board, row, col_placed, current_checker):
            print(f"Player {current_checker} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
