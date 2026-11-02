import os
import random
import string

# === CONSTANTS ===
ROWS = 6
COLS = 7
MAX_COLS = 26
PLAYER_NUM = 2  # Can be 2-5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    print('  ' + '   '.join(string.ascii_uppercase[:cols]))
    # Print top border
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    return [c for c in range(len(board[0])) if board[0][c] == ' ']

def get_column_index(input_str, cols):
    if len(input_str) != 1:
        return -1
    letter = input_str.upper()
    if letter in string.ascii_uppercase[:cols]:
        return ord(letter) - ord('A')
    return -1

def drop_checker(board, col, player_checker):
    rows = len(board)
    # Start from bottom
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player_checker
            return row, col
    return None, None  # Column full

def is_winning_move(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    # Setup game
    if COLS > MAX_COLS:
        print(f"Max columns is {MAX_COLS}")
        return
    if not (2 <= PLAYER_NUM <= 5):
        print("Player number must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYER_NUM]
    player_names = [f"Player {c}" for c in players]

    # Random first player
    current_player = random.randint(0, PLAYER_NUM - 1)

    clear_screen()
    print_board(board)
    print(f"{player_names[current_player]}, you start!")

    while True:
        current_checker = players[current_player]
        player_label = player_names[current_player]

        # Print board
        clear_screen()
        print_board(board)

        # Check for draw before move
        if is_board_full(board):
            print("The game is a draw!")
            break

        print(f"{player_label} ({current_checker}), please enter a column:")

        valid_move = False
        invalid_input = False
        invalid_full_col = False
        col = None
        while not valid_move:
            move = input().strip().upper()
            col = get_column_index(move, COLS)
            if col == -1:
                print("Invalid input. Please enter a valid column letter:")
                continue
            if board[0][col] != ' ':
                print("Column is full. You lose your turn!")
                invalid_full_col = True
                break  # Lose turn
            valid_move = True

        if invalid_full_col:
            # skip to next player
            current_player = (current_player + 1) % PLAYER_NUM
            continue

        # Drop checker
        row, _ = drop_checker(board, col, current_checker)

        # Check for win
        if is_winning_move(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"{player_label} ({current_checker}) won!")
            break

        # Check for draw after move
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % PLAYER_NUM

if __name__ == '__main__':
    main()
