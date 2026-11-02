import os
import random
import string

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_COUNT = 4
TOKENS = ['X', 'O', 'V', 'H', 'M']  # In order for up to 5 players

# Ensure limits
COLS = max(1, min(COLS, 26))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, 5))

# Initialize board with spaces
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board():
    clear_screen()
    # Header letters
    letters = string.ascii_uppercase[:COLS]
    print('  ' + '   '.join(list(letters)))
    # Top border
    print('+' + '---+' * COLS)
    # Rows
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {cell} ' for cell in row_cells) + '|')
        print('+' + '---+' * COLS)

def get_column_input(current_token):
    # Keep asking until a valid column letter is provided
    while True:
        user_input = input(f'Player {current_token}, please enter a column: ').strip().upper()
        if len(user_input) != 1:
            print('Invalid input. Please enter a single letter.')
            continue
        if user_input < 'A' or user_input >= chr(ord('A') + COLS):
            print('Invalid column. Please choose a letter shown at the top of the board.')
            continue
        return ord(user_input) - ord('A')

def find_row_for_drop(col):
    # Find the lowest available row in the given column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None  # Column full

def place_checker(col, token):
    row = find_row_for_drop(col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)

def count_in_direction(start_r, start_c, dr, dc, token):
    count = 0
    r, c = start_r, start_c
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count

def check_win(r, c, token):
    # Check four directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count both ways from the placed checker
        total = 1
        total += count_in_direction(r + dr, c + dc, dr, dc, token)
        total += count_in_direction(r - dr, c - dc, -dr, -dc, token)
        if total >= WIN_COUNT:
            return True
    return False

def is_draw():
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    # Prepare players
    players = TOKENS[:NUM_PLAYERS]
    current_index = random.randrange(NUM_PLAYERS)

    # Show empty board before starting
    print_board()

    while True:
        current_token = players[current_index]
        col = get_column_input(current_token)

        # Try to place the checker
        result = place_checker(col, current_token)
        if result is None:
            # Column full, turn is lost
            print(f'Column {chr(ord("A") + col)} is full. Player {current_token} loses the turn.')
            input('Press Enter to continue...')
            # Next player
            current_index = (current_index + 1) % NUM_PLAYERS
            print_board()
            continue

        # Successfully placed
        r, c = result
        print_board()

        # Check for win
        if check_win(r, c, current_token):
            print(f'Player {current_token} won!')
            break

        # Check for draw
        if is_draw():
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
