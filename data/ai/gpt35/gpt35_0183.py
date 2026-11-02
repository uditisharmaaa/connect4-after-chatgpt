import os
import random
import string

# Constants: Board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column labels A..G (or more)
    col_labels = string.ascii_uppercase[:len(board[0])]
    print('  ' + '   '.join(col_labels))
    # Print the board with borders between cells
    horizontal_line = '+' + '+'.join(['---'] * len(board[0])) + '+'
    for row in board:
        print(horizontal_line)
        print('| ' + ' | '.join(row) + ' |')
    print(horizontal_line)

def is_valid_column(input_str, cols):
    if len(input_str) != 1:
        return False
    if input_str not in string.ascii_uppercase[:cols]:
        return False
    return True

def get_column_index(col_char):
    return string.ascii_uppercase.index(col_char)

def place_checker(board, col_idx, checker):
    # Place checker at lowest free row in the given column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full
    return None, None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # If any cell in top row is empty, board is not full
    for c in range(len(board[0])):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    
    # Randomly select starting player index
    current_player_idx = random.randint(0, PLAYERS -1)

    print_board(board)

    while True:
        checker = players[current_player_idx]
        prompt = f"Player {checker}, please enter a column: "
        col_char = input(prompt).strip().upper()

        if not is_valid_column(col_char, COLS):
            # Invalid input: not a single uppercase letter or out of range
            continue

        col_idx = get_column_index(col_char)

        # Try placing checker
        row_idx, col_idx_placed = place_checker(board, col_idx, checker)
        if row_idx is None:
            # Column full, player loses turn, i.e. move to next player
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        print_board(board)

        # Check win
        if check_win(board, row_idx, col_idx_placed, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
