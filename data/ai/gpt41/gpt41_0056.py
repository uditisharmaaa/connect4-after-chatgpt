import os
import random
import string

# === CONSTANTS ===
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # For labeling columns with letters up to Z
PLAYERS = 2  # Set to 2 for submission, but code supports 2-5
CHECKERS = ["X", "O", "V", "H", "M"]

# === FUNCTIONS ===

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    cols = len(board[0])
    header = "  " + "   ".join([string.ascii_uppercase[c] for c in range(cols)])
    separator = "+" + "---+" * cols
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)

def get_valid_columns(board):
    valid_cols = []
    for c in range(len(board[0])):
        if board[0][c] == " ":
            valid_cols.append(c)
    return valid_cols

def get_move_input(current_player_checker, valid_columns, columns):
    while True:
        move = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if len(move) != 1 or move not in string.ascii_uppercase[:columns]:
            print("Invalid input. Please enter a column letter from the board.")
            continue
        col_index = string.ascii_uppercase.index(move)
        if col_index not in valid_columns:
            print("Column is full. Please choose another column.")
            continue
        return col_index

def place_checker(board, column, checker):
    # Place checker in the lowest available row in the specified column
    for row in reversed(range(len(board))):
        if board[row][column] == " ":
            board[row][column] = checker
            return row, column  # Return the position for win checking

def check_win(board, checker, row, col):
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1  # The checker just played
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            if count == 4:
                return True
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            if count == 4:
                return True
            r -= dr
            c -= dc
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    random.seed()  # Initialize random number generator
    
    # Use only as many checkers as there are players
    player_checkers = CHECKERS[:PLAYERS]
    
    board = create_board(ROWS, COLUMNS)

    # Randomly select starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    clear_screen()
    print_board(board)

    game_over = False
    while not game_over:
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("Game ended in a draw!")
            break
        current_checker = player_checkers[current_player]
        col_index = get_move_input(current_checker, valid_columns, COLUMNS)
        row, col = place_checker(board, col_index, current_checker)

        clear_screen()
        print_board(board)

        if check_win(board, current_checker, row, col):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("Game ended in a draw!")
            game_over = True
        else:
            # Change to next player
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
