import os
import random
import sys

# CONSTANTS
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_COLS = 26  # For boards up to 26 columns
NUM_PLAYERS = 2  # Change this up to 5 for testing
CHECKERS = ['X', 'O', 'V', 'H', 'M']
EMPTY_CELL = ' '

# Helper function for clearing the console screen
def clear_screen():
    os.system('clear')  # On Windows systems, use 'cls'

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    rows = len(board)
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(cols)])
    divider = '+' + ('---+' * cols)
    print(header)
    print(divider)
    for r in range(rows):
        row_str = '|'
        for c in range(cols):
            row_str += f' {board[r][c]} |'
        print(row_str)
        print(divider)

def get_valid_columns(board):
    valid_cols = []
    for c in range(len(board[0])):
        if board[0][c] == EMPTY_CELL:
            col_letter = chr(ord('A') + c)
            valid_cols.append(col_letter)
    return valid_cols

def get_player_input(player_checker, board):
    cols = len(board[0])
    valid_cols = get_valid_columns(board)
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single column letter.")
            continue
        col_idx = ord(user_input) - ord('A')
        if col_idx < 0 or col_idx >= cols:
            print("Invalid column letter. Please select a valid column.")
            continue
        if user_input not in valid_cols:
            if board[0][col_idx] != EMPTY_CELL:
                print("This column is full. You lose your turn.")
                return None  # Lose turn if column is full (per instructions)
            else:
                print("Invalid column. Please select another one.")
            continue
        return col_idx

def place_checker(board, col_idx, checker):
    rows = len(board)
    # Start from the bottom row and go up
    for row in range(rows-1, -1, -1):
        if board[row][col_idx] == EMPTY_CELL:
            board[row][col_idx] = checker
            return row, col_idx
    # This case should be handled before, but just in case
    return None

def check_win(board, last_row, last_col, checker):
    rows = len(board)
    cols = len(board[0])

    def count_dir(dr, dc):
        count = 0
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions (dr, dc): horizontal, vertical, diag \, diag /
    directions = [ (0, 1), (1, 0), (1, 1), (1, -1) ]
    for dr, dc in directions:
        count = 1  # Current checker
        count += count_dir(dr, dc)
        count += count_dir(-dr, -dc)
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != EMPTY_CELL for c in range(len(board[0])))

def main():
    # Set up game
    board = create_board(BOARD_ROWS, BOARD_COLS)
    player_count = NUM_PLAYERS
    if player_count < 2 or player_count > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)
    player_checkers = CHECKERS[:player_count]
    first_player_idx = random.randint(0, player_count - 1)
    current_idx = first_player_idx

    # Show initial board
    clear_screen()
    print_board(board)

    while True:
        current_checker = player_checkers[current_idx]

        col_idx = get_player_input(current_checker, board)
        clear_screen()

        if col_idx is not None:
            # Place checker and get position
            pos = place_checker(board, col_idx, current_checker)
            print_board(board)

            if pos:
                row, col = pos
                if check_win(board, row, col, current_checker):
                    print(f"Player {current_checker} won!")
                    break
                elif is_draw(board):
                    print("The game is a draw!")
                    break
        else:
            # Show board after losing the turn (column full)
            print_board(board)

        # Next player
        current_idx = (current_idx + 1) % player_count

if __name__ == '__main__':
    main()
