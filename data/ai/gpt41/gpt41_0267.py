import os
import random
import string

# Constants (can be changed for different board sizes and player counts)
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26  # So columns can be labeled A-Z
PLAYERS = 2  # between 2 and 5

PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')  # On Windows use 'cls'

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "---+" * cols
    print(header)
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def get_valid_columns(board):
    return [
        idx for idx in range(len(board[0]))
        if board[0][idx] == ' '
    ]

def get_col_from_letter(letter):
    if letter in string.ascii_uppercase:
        return ord(letter) - ord('A')
    else:
        return -1

def drop_checker(board, col, checker):
    # Places checker in the chosen column, returns the row index where placed
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None  # Should not happen if checked before

def is_full(board):
    return all(cell != ' ' for cell in board[0])

def check_direction(board, row, col, dr, dc, checker):
    rows, cols = len(board), len(board[0])
    count = 1
    # one direction
    r, c = row + dr, col + dc
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    # opposite direction
    r, c = row - dr, col - dc
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= dr
        c -= dc
    return count >= 4

def check_for_win(board, row, col, checker):
    # Checks all directions
    return (
        check_direction(board, row, col, 0, 1, checker) or  # Horizontal
        check_direction(board, row, col, 1, 0, checker) or  # Vertical
        check_direction(board, row, col, 1, 1, checker) or  # Diagonal /
        check_direction(board, row, col, 1, -1, checker)    # Diagonal \
    )

def main():
    # Set up
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)
    while True:
        current_checker = players[current_player_idx]
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("Game is a draw!")
            break
        # Input phase
        while True:
            try:
                print(f"Player {current_checker}, please enter a column:")
                col_input = input().strip().upper()
                if len(col_input) != 1:
                    raise ValueError("Please enter a single column letter.")
                col = get_col_from_letter(col_input)
                if col == -1 or col >= NUM_COLS:
                    raise ValueError("Invalid column letter.")
                if col not in valid_columns:
                    if board[0][col] != ' ':
                        print("Column is full - you lose your turn.")
                        col = None
                        break
                    else:
                        raise ValueError("Column is not valid.")
                break  # Valid input
            except ValueError as e:
                print(e)
        if col is None:
            # Player loses turn
            current_player_idx = (current_player_idx + 1) % PLAYERS
            clear_screen()
            print_board(board)
            continue
        # Place checker
        row = drop_checker(board, col, current_checker)
        clear_screen()
        print_board(board)
        # Check for win
        if check_for_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        # Check for draw
        if is_full(board):
            print("Game is a draw!")
            break
        # Next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == '__main__':
    main()
