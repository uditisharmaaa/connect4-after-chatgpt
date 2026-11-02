import os
import random
import string

# Constants (can be changed for different board sizes or #players)
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2                                    # change to 2-5 as needed
CHECKERS = ['X', 'O', 'V', 'H', 'M']              # max 5 players
WIN_STREAK = 4

def clear_screen():
    # Works for Linux/Unix
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Print column headers
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def is_valid_column_input(col_input, cols):
    if len(col_input) != 1:
        return False
    if col_input not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_available_row(board, col):
    # Return the index of the lowest available row in the chosen column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_STREAK:
            return True
    return False

def get_player_input(player_checker, board):
    cols = len(board[0])
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if not is_valid_column_input(col_input, cols):
            print(f"Invalid input. Please enter a letter from A to {string.ascii_uppercase[cols-1]}.")
            continue
        col_idx = string.ascii_uppercase.index(col_input)
        if board[0][col_idx] != ' ':
            print("Column is full. You lose your turn!")
            return None
        return col_idx

def main():
    # Set up
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {player_symbols[current_player]} starts!")
    input("Press Enter to start...")

    while True:
        print_board(board)

        col_idx = get_player_input(player_symbols[current_player], board)
        if col_idx is None:
            # If the column is full, skip to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row_idx = get_available_row(board, col_idx)
        if row_idx is None:
            # Shouldn't happen because of col full check, but just in case
            print("Unexpected error: no available row. Skipping turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        board[row_idx][col_idx] = player_symbols[current_player]

        # Check for win
        if check_win(board, row_idx, col_idx, player_symbols[current_player]):
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("Draw! The board is full.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == '__main__':
    main()
