import os
import random
import string

# ==== CONSTANT VARIABLES ====
ROWS = 6
COLUMNS = 7  # Max 26!
NUM_PLAYERS = 2  # Can be 2-5

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# ==== HELPER FUNCTIONS ====

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board, column_labels):
    # Print column headers
    print("  " + "   ".join(column_labels))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column_input(occupied_columns, column_labels):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input not in column_labels:
            print("Invalid input! Please enter a valid column letter.")
            continue
        col_idx = column_labels.index(user_input)
        if occupied_columns[col_idx]:
            print("Column is full! You lose your turn.")
            return None  # Indicate a lost turn
        return col_idx

def drop_checker(board, col_idx, checker):
    for row in reversed(board):
        if row[col_idx] == " ":
            row[col_idx] = checker
            return board.index(row), col_idx
    return None  # should not happen if checked correctly

def is_column_full(board, col_idx):
    return all(row[col_idx] != " " for row in board)

def check_win(board, row_idx, col_idx, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # include the just-placed checker itself
        for dir in [1, -1]:  # check both ways in this direction
            r, c = row_idx, col_idx
            while True:
                r += dr * dir
                c += dc * dir
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_is_full(board):
    return all(cell != " " for row in board for cell in row)

# ==== MAIN LOGIC ====

def main():
    # Set up
    board = create_board()
    column_labels = list(string.ascii_uppercase[:COLUMNS])
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_idx = random.randint(0, NUM_PLAYERS - 1)
    turn_order = [i for i in range(NUM_PLAYERS)]
    
    # Initial board
    clear_screen()
    print_board(board, column_labels)
    print(f"Player {players[current_idx]} goes first!\n")

    while True:
        occupied_columns = [is_column_full(board, col) for col in range(COLUMNS)]
        player = players[current_idx]
        print(f"Player {player}, ", end="")
        col_idx = get_valid_column_input(occupied_columns, column_labels)
        if col_idx is None:
            # Skip player if column is full
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Place checker
        row_idx, col_idx = drop_checker(board, col_idx, player)
        clear_screen()
        print_board(board, column_labels)

        # Check for win
        if check_win(board, row_idx, col_idx, player):
            print(f"Player {player} won!")
            break

        # Check for draw
        if board_is_full(board):
            print("It's a draw!")
            break

        # Next player
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
