import os
import random
import string

# === GLOBAL CONSTANTS ===
ROWS = 6           # number of rows
COLS = 7           # number of columns (max 26)
PLAYERS = 2        # between 2 and 5

PLAYER_CHARS = ['X', 'O', 'V', 'H', 'M']

# === BOARD INITIALIZATION ===
def create_board(rows, cols):
    # board[row][col], row 0 is top
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # clears the screen before printing
    cols = len(board[0])
    rows = len(board)
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    label_row = '  ' + '   '.join(col_labels)
    print(label_row)
    # Print top border
    print('+' + '---+' * cols)
    for row in board:
        # Print row with | separators
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        # Print row border
        print('+' + '---+' * cols)

def choose_first_player(num_players):
    return random.randint(0, num_players - 1)

def get_player_checker(player_number):
    return PLAYER_CHARS[player_number]

def get_valid_columns(board):
    # A column is valid if its top cell is empty
    return [i for i in range(len(board[0])) if board[0][i] == ' ']

def column_full(board, col):
    return board[0][col] != ' '

def is_board_full(board):
    return all(cell != ' ' for cell in board[0])

def get_column_index(input_string, cols):
    # Expects a single uppercase letter
    if len(input_string) != 1:
        return -1
    ch = input_string[0]
    if ch not in string.ascii_uppercase[:cols]:
        return -1
    return string.ascii_uppercase.index(ch)

def get_player_input(board, cols):
    valid = False
    while not valid:
        user_input = input("Please enter a column: ").strip().upper()
        col = get_column_index(user_input, cols)
        if col == -1:
            print("Invalid column. Please use a letter between A and {}.".format(string.ascii_uppercase[cols-1]))
            continue
        if column_full(board, col):
            print("That column is full. You lose your turn.")
            return None  # Indicate that player loses turn
        valid = True
    return col

def place_checker(board, col, checker):
    rows = len(board)
    for row in range(rows-1, -1, -1):  # Start from last row upwards
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col  # Return the position where checker was placed
    # Should not reach here (guarded by column_full before)

def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Check all directions: horizontal, vertical, diag-right-down (\), diag-left-down (/)
    for r in range(rows):
        for c in range(cols):
            # Only check from the cell if it is the current player's marker
            if board[r][c] != checker:
                continue
            # Horizontal
            if c + 3 < cols and all(board[r][c+i] == checker for i in range(4)):
                return True
            # Vertical
            if r + 3 < rows and all(board[r+i][c] == checker for i in range(4)):
                return True
            # Diagonal down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            # Diagonal down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def main():
    # Ensure settings are within bounds
    assert 2 <= PLAYERS <= 5, "Players must be between 2 and 5"
    assert 4 <= ROWS <= 99 and 4 <= COLS <= 26, "Rows and columns out of allowed range"

    board = create_board(ROWS, COLS)
    current_player = choose_first_player(PLAYERS)
    player_checkers = PLAYER_CHARS[:PLAYERS]

    print_board(board)
    print("Player {} ({}) goes first!".format(player_checkers[current_player], player_checkers[current_player]))

    winner = None
    moves = 0
    while True:
        checker = player_checkers[current_player]
        print_board(board)
        print("Player {}, please enter a column:".format(checker))
        col = get_player_input(board, COLS)
        if col is None:
            # Player loses turn, as per description
            current_player = (current_player + 1) % PLAYERS
            continue
        row, col = place_checker(board, col, checker)
        moves += 1
        if check_winner(board, checker):
            print_board(board)
            print("Player {} won!".format(checker))
            break
        if is_board_full(board):
            print_board(board)
            print("The game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
