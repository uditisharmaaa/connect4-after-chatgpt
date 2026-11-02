import os
import random
import string

# ==== CONSTANTS ====
ROWS = 6
COLUMNS = 7
PLAYERS = 2           # Must be between 2 and 5
CONNECT_N = 4         # Number of checkers in a row needed to win
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ==== FUNCTIONS ====

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_valid_columns(board):
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols

def input_column(valid_cols, col_labels):
    while True:
        move = input("Please enter a column: ").strip().upper()
        if len(move) != 1 or move not in col_labels:
            print("Invalid input. Please use column letters (e.g., A, B, ...).")
            continue
        idx = col_labels.index(move)
        if idx not in valid_cols:
            print("Column is full or invalid. Please choose another column.")
            continue
        return idx

def drop_checker(board, col, checker):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Column is full

def check_win(board, row, col, checker):
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= CONNECT_N:
            return True
    return False

def check_draw(board):
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def play_game():
    rows, cols = ROWS, COLUMNS
    n_players = PLAYERS
    checkers = CHECKERS[:n_players]
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    board = create_board(rows, cols)

    # Choose random starting player
    current_player = random.randint(0, n_players - 1)

    clear_screen()
    print_board(board)

    while True:
        checker = checkers[current_player]
        print(f"Player {checker},", end=' ')
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("The board is full! The game is a draw.")
            break

        col = None
        col_labels_valid = [col_labels[i] for i in valid_cols]
        # Input loop handles invalid input until valid
        col = input_column(valid_cols, col_labels)
        result = drop_checker(board, col, checker)
        if result is None:
            print("Column is full. You lose your turn.") # Invalid turn
            current_player = (current_player + 1) % n_players
            continue
        row, col = result

        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The board is full! The game is a draw.")
            break

        # Switch player
        current_player = (current_player + 1) % n_players

# ==== MAIN ==== #
if __name__ == "__main__":
    play_game()
