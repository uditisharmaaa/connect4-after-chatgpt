import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
WIN_LENGTH = 4
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Settings for this submission
NUM_PLAYERS = 2
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(headers))
    # Print board rows with separators
    line_sep = '+' + '---+' * cols
    for r in range(rows):
        print(line_sep)
        row_str = '|'
        for c in range(cols):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print(line_sep)

def is_valid_column(col_char, cols):
    if len(col_char) != 1 or not col_char.isalpha():
        return False
    col = ord(col_char) - ord('A')
    return 0 <= col < cols

def get_valid_input(player, board):
    cols = len(board[0])
    while True:
        user_input = input(f"Player {player}, please enter a column: ").upper().strip()
        if not is_valid_column(user_input, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = ord(user_input) - ord('A')
        # Check if column is already full
        if board[0][col] != ' ':
            # Turn lost, so print message and return None
            print(f"Column {user_input} is full. You lose your turn!")
            return None
        return col

def place_checker(board, col, player):
    rows = len(board)
    # Start from bottom row up, place at first empty cell
    for r in range(rows-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return r, col

def check_win(board, player):
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc) and board[nr][nc] == player:
                    count += 1
                    if count == WIN_LENGTH:
                        return True
                    nr += dr
                    nc += dc
    return False

def check_draw(board):
    # Draw if top row has no empty spaces
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS -1)
    total_moves = 0
    max_moves = ROWS * COLS

    print_board(board)

    while True:
        player = PLAYERS[current_player_index]
        col = get_valid_input(player, board)
        if col is None:
            # Column full - turn lost
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        place_checker(board, col, player)
        total_moves += 1
        print_board(board)

        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if total_moves == max_moves or check_draw(board):
            print("It's a draw!")
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
