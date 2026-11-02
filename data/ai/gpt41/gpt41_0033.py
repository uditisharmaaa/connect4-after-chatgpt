import os
import random
import string

# --------- CONSTANT VARIABLES ---------------
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Can be set to 2, 3, 4, or 5
CONNECT_N = 4

CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --------- BOARD INITIALIZATION -------------

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')  # For Windows, use 'cls'

def print_board(board):
    # Print column labels
    col_labels = '  ' + '   '.join([chr(ord('A') + i) for i in range(COLUMNS)])
    print(col_labels)
    # Print top border
    print('+' + '---+' * COLUMNS)
    # Print each row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

# --------- GAME LOGIC ----------------------

def get_player_input(player, board):
    while True:
        move = input(f"Player {player}, please enter a column: ").strip()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single column letter.")
            continue
        col_letter = move.upper()
        col_index = ord(col_letter) - ord('A')
        if col_index < 0 or col_index >= COLUMNS:
            print("Invalid column letter. Try again.")
            continue
        # If column is full
        if board[0][col_index] != ' ':
            print("Column is full. You lose your turn.")
            return None  # Lose turn if column is full
        return col_index

def place_checker(board, col, checker):
    # From bottom row up, find the first empty cell
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Shouldn't happen due to check earlier

def check_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - CONNECT_N + 1):
            if all(board[row][col + k] == checker for k in range(CONNECT_N)):
                return True

    # Vertical check
    for row in range(ROWS - CONNECT_N + 1):
        for col in range(COLUMNS):
            if all(board[row + k][col] == checker for k in range(CONNECT_N)):
                return True

    # Diagonal down-right
    for row in range(ROWS - CONNECT_N + 1):
        for col in range(COLUMNS - CONNECT_N + 1):
            if all(board[row + k][col + k] == checker for k in range(CONNECT_N)):
                return True

    # Diagonal up-right
    for row in range(CONNECT_N - 1, ROWS):
        for col in range(COLUMNS - CONNECT_N + 1):
            if all(board[row - k][col + k] == checker for k in range(CONNECT_N)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# --------- MAIN GAME LOOP ------------------

def play_game():
    board = create_board()
    player_checkers = CHECKERS[:PLAYERS]

    # Select random player
    current_player = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        checker = player_checkers[current_player]
        print(f"Player {checker}'s turn.")
        col_index = get_player_input(checker, board)
        if col_index is not None:
            # Place checker
            place_checker(board, col_index, checker)
        clear_screen()
        print_board(board)
        # Check for win
        if col_index is not None:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
        # Check for draw
        if check_draw(board):
            print("Game is a draw.")
            break
        # Next player
        current_player = (current_player + 1) % PLAYERS

# --------- ENTRY POINT --------------------

if __name__ == "__main__":
    play_game()
