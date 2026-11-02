import random
import os
import string

# ====== CONSTANTS ======
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2 # Change to 3, 4, 5 for more players
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

# ====== BOARD UTILITIES ======
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # use 'cls' for Windows systems
    cols = len(board[0])
    # Print column headers
    headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(headers)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * cols)

def is_column_full(board, col):
    return board[0][col] != ' '

def get_lowest_empty_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_valid_column(col_input, cols):
    return (len(col_input) == 1 
            and col_input.isalpha() 
            and col_input.isupper() 
            and ord(col_input) - ord('A') < cols)

# ====== GAME LOGIC ======
def place_checker(board, col, checker):
    row = get_lowest_empty_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row, col
    else:
        return None

def check_win(board, row, col, checker):
    def count(d_row, d_col):
        r, c, count = row + d_row, col + d_col, 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += d_row
            c += d_col
        return count

    # Check all directions: horizontal, vertical, 2 diagonals
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)] # right, down, diag-down-right, diag-up-right
    for d_row, d_col in directions:
        total = 1 + count(d_row, d_col) + count(-d_row, -d_col)
        if total >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

# ====== MAIN GAME LOOP ======
def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    print(f"Player {CHECKERS[current_player]} is randomly chosen to start.")
    input("Press Enter to start...")

    game_over = False
    while not game_over:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        # Input validation
        col_input = input().strip().upper()
        while True:
            if not is_valid_column(col_input, COLUMNS):
                print(f"Invalid column. Enter a letter A-{string.ascii_uppercase[COLUMNS-1]}:")
            else:
                col = ord(col_input) - ord('A')
                if is_column_full(board, col):
                    print("That column is full and you lose your turn.")
                    col = None
                    break  # skip placing
                else:
                    break
            col_input = input().strip().upper()
        
        if col is not None:
            pos = place_checker(board, col, CHECKERS[current_player])
            row, col_placed = pos
            # Check for win
            if check_win(board, row, col_placed, CHECKERS[current_player]):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                game_over = True
                continue
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
                continue
        
        # Next turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
