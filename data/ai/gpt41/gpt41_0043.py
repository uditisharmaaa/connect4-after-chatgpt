import os
import random
import string

# Constants for game, can be changed
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # between 2 and 5

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Board column labels: 'A', 'B', ..., up to maximum columns 26 ('Z')
COLUMN_LABELS = list(string.ascii_uppercase)

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    # Create a 2D board: list of lists, rows x cols, initialized with ' '
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headings
    print("  " + "   ".join(COLUMN_LABELS[:cols]))
    print("+" + "---+" * cols)
    # Print each row
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def get_player_input(current_player, board):
    cols = len(board[0])
    valid_labels = COLUMN_LABELS[:cols]
    while True:
        move = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in valid_labels:
            print(f"Invalid input. Please enter a letter between {valid_labels[0]} and {valid_labels[-1]}.")
            continue
        col = valid_labels.index(move)
        # Check if the column is not completely full
        if board[0][col] != ' ':
            print("This column is full! You lose your turn.")
            return None  # Lose this turn, as per assignment
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest unoccupied row
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Shouldn't happen, as we verify column beforehand

def check_win(board, row, col, checker):
    # Helper function for checking a particular direction
    def count_in_direction(dx, dy):
        count = 0
        x, y = row + dx, col + dy
        while 0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == checker:
            count += 1
            x += dx
            y += dy
        return count

    # Directions: [(row step, col step), ...]
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]
    for dr, dc in directions:
        count = 1  # Count the placed checker itself
        count += count_in_direction(dr, dc)
        count += count_in_direction(-dr, -dc)
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    rows = NUM_ROWS
    cols = NUM_COLS
    num_players = NUM_PLAYERS
    checkers = CHECKERS[:num_players]

    # Randomly determine first player
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board(rows, cols)

    # Initial display
    clear_screen()
    print_board(board)
    print()
    print(f"Player {checkers[current_player_idx]} will start!")
    print()

    while True:
        player_checker = checkers[current_player_idx]
        col = get_player_input(player_checker, board)
        clear_screen()
        if col is not None:
            row_col = place_checker(board, col, player_checker)
            print_board(board)
            if row_col:
                row, col_actual = row_col
                if check_win(board, row, col_actual, player_checker):
                    print(f"Player {player_checker} won!")
                    break
            if check_draw(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
