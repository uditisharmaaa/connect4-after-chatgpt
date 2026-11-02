import os
import random
import string

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column header (A..)
    letters = list(string.ascii_uppercase[:cols])
    header = '  ' + '   '.join(letters)
    separator = '+' + '---+' * cols

    print(header)
    print(separator)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print('|' + '|'.join(f' {ch} ' for ch in row_cells) + '|')
        print(separator)


def get_column_input(cols):
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        try:
            s = input().strip()
        except EOFError:
            s = ''
        if len(s) == 1:
            ch = s.upper()
            if ch in valid_letters:
                return ord(ch) - ord('A')
        print(f"Invalid input. Please enter a column letter between A and {valid_letters[-1]}:")


def drop_checker(board, col, checker):
    # Returns row index where placed, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return None


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc) right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                cnt = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    cnt += 1
                    if cnt == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def main():
    # Basic constraints
    cols = max(1, min(COLS, 26))
    rows = max(1, ROWS)
    players = max(2, min(NUM_PLAYERS, 5))
    checkers = CHECKERS[:players]

    board = create_board(rows, cols)

    # Random first player
    current_player = random.randint(0, players - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        current_checker = checkers[current_player]
        print(f"Player {current_checker}, please enter a column:")
        col = get_column_input(cols)

        placed_row = drop_checker(board, col, current_checker)
        if placed_row is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Turn lost.")
            # Next player's turn
            current_player = (current_player + 1) % players
            continue

        # After a successful move, check for win/draw
        if check_winner(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % players

        # Show updated board for the next player
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
