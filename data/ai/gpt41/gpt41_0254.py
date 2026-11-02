import os
import random
import string

# ----- CONFIGURATION CONSTANTS -----
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ----- BOARD SETUP -----
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Or use 'cls' on Windows
    cols_str = '  ' + '   '.join(string.ascii_uppercase[:len(board[0])])
    print(cols_str)
    print('+' + '---+' * len(board[0]))
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print('+' + '---+' * len(board[0]))

# ----- INPUT HANDLING -----
def get_valid_column(board, current_player):
    cols_labels = string.ascii_uppercase[:len(board[0])]
    while True:
        entry = input(f"Player {current_player}, please enter a column: ").strip().upper()
        # Validate input length & char
        if len(entry) != 1 or entry not in cols_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = cols_labels.index(entry)
        # Check if column is full
        if board[0][col] != ' ':
            print("That column is full. You lose your turn.")
            return None
        return col

# ----- GAME LOGIC -----
def place_checker(board, col, checker):
    # Place the checker in the lowest empty row in the given column
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None, None

def check_win(board, player_char):
    rows, cols = len(board), len(board[0])

    # HORIZONTAL
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_char for i in range(4)):
                return True
    # VERTICAL
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == player_char for i in range(4)):
                return True
    # DIAGONAL DOWN-RIGHT
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_char for i in range(4)):
                return True
    # DIAGONAL UP-RIGHT
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_char for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(len(board[0])))

# ----- MAIN GAME LOOP -----
def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        current_player = players[current]
        col = get_valid_column(board, current_player)
        if col is None:
            # Column full, player loses turn
            current = (current + 1) % NUM_PLAYERS
            continue

        row, col_pos = place_checker(board, col, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # Next turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
