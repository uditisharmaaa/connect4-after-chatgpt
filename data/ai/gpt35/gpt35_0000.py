import os
import random

# Constants
ROWS = 6
COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_COUNT = 2  # Set number of players here (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    # Print board rows
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print("+" + "---+" * COLS)

def is_valid_column(col_letter):
    return col_letter in COLUMN_LABELS

def column_index(col_letter):
    return COLUMN_LABELS.index(col_letter)

def column_full(board, col_idx):
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in lowest available row in column, if possible
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Column full

def check_win(board, row, col, checker):
    # Directions: horizontal, vertical, diag \ and diag /
    directions = [
        (0,1),  # horizontal right
        (1,0),  # vertical down
        (1,1),  # diagonal down-right
        (1,-1), # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def check_draw(board):
    # Draw if top row is full across all columns
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def get_player_input(player_checker):
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not is_valid_column(inp):
            print("Invalid column. Please enter a valid column letter.")
            continue
        return inp

def main():
    # Validate constants
    if not (2 <= PLAYERS_COUNT <= 5):
        print(f"Error: PLAYERS_COUNT must be between 2 and 5, got {PLAYERS_COUNT}.")
        return
    
    board = create_board()
    players = CHECKERS[:PLAYERS_COUNT]

    # Randomly select first player index
    current_player_idx = random.randrange(PLAYERS_COUNT)

    print_board(board)

    while True:
        player_checker = players[current_player_idx]
        
        col_letter = get_player_input(player_checker)
        col_idx = column_index(col_letter)

        if column_full(board, col_idx):
            print(f"Column {col_letter} is full. Player {player_checker} loses this turn.")
            # Lose this turn, just go to next player without placing checker
        else:
            pos = place_checker(board, col_idx, player_checker)
            print_board(board)
            if pos is not None:
                row_played, col_played = pos
                if check_win(board, row_played, col_played, player_checker):
                    print(f"Player {player_checker} won!")
                    break
                elif check_draw(board):
                    print("The game is a draw!")
                    break
            else:
                # Should never get here due to column_full check
                print(f"Unexpected error placing checker for player {player_checker} in column {col_letter}.")

        # Move to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
