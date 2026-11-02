import os
import random
import string

# -------------------
# CONSTANT VARIABLES
# -------------------
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # between 2 and 5

# Checker symbols for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# Board column labels (A, B, ..., Z)
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

# -------------------
# HELPER FUNCTIONS
# -------------------

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, cols=COLUMNS):
    '''Create an empty board as a list of lists.'''
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    '''Prints the board according to specified format.'''
    # Print column column headers
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_valid_input(board):
    '''Prompts user for a valid column until a valid choice is made. Returns column index (int).'''
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1 or user_input not in COLUMN_LABELS:
            print(f"Invalid input. Please enter one letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}:")
            continue
        col = COLUMN_LABELS.index(user_input)
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full. You lose your turn.")
            return None  # Special behavior: lose turn as per assignment
        return col

def drop_checker(board, col, checker):
    '''Place the checker in the lowest empty cell in the selected column.'''
    for row in reversed(range(ROWS)):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col  # Return coordinates of the placed checker
    return None  # Column full: should not happen, handled before

def check_win(board, last_row, last_col, checker):
    '''Check all directions from last move for a win.'''
    directions = [ (0, 1), (1, 0), (1, 1), (1, -1) ]  # horizontal, vertical, diag \, diag /
    for dr, dc in directions:
        count = 1
        # Check in the + direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the - direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    '''Returns True if the board is full and no winner.'''
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def switch_player(current_index, total_players):
    return (current_index + 1) % total_players

# -------------------
# MAIN GAME FUNCTION
# -------------------

def play_connect_four():
    board = create_board()
    # Randomly select starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    clear_screen()
    print_board(board)
    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")
        col = get_valid_input(board)
        if col is None:
            # Column full, player loses turn
            current_player = switch_player(current_player, NUM_PLAYERS)
            clear_screen()
            print_board(board)
            continue
        row, col = drop_checker(board, col, player_checker)
        clear_screen()
        print_board(board)
        if check_win(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            current_player = switch_player(current_player, NUM_PLAYERS)

# -------------------
# RUN GAME
# -------------------

if __name__ == "__main__":
    play_connect_four()
